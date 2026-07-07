from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import uuid
from .models import Conversation, Message
from .serializers import ConversationSerializer

SYSTEM_PROMPT = "You are CourierBot AI, a specialized expert assistant for Courier Services and Inventory Management in Pakistan. Answer questions about TCS, Leopards, PostEx, BlueEx couriers, inventory management, stock control, warehouse operations, international shipping, COD, parcel tracking. FIFO/LIFO/EOQ/ABC Analysis. Respond in same language as user."
import os
API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
FALLBACK_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "nvidia/nemotron-3-nano-30b-a3b:free",
]


@api_view(["GET"])
def get_models(request):
    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
        )
        data = resp.json()
        all_models = data.get("data", [])
        free_models = []
        for m in all_models:
            pricing = m.get("pricing", {})
            try:
                prompt_price = float(pricing.get("prompt", "1"))
                completion_price = float(pricing.get("completion", "1"))
            except:
                continue
            if prompt_price == 0 and completion_price == 0:
                free_models.append({
                    "id": m.get("id"),
                    "name": m.get("name", m.get("id")),
                    "provider": m.get("id", "").split("/")[0].upper(),
                    "context": m.get("context_length", 0),
                })
        free_models.sort(key=lambda x: x["name"])
        return Response(free_models)
    except Exception as e:
        print("MODELS ERROR:", str(e))
        return Response([
            {"id": "openrouter/free", "name": "Auto (Best Free Model)", "provider": "OpenRouter", "context": 0}
        ])


@csrf_exempt
@api_view(["POST"])
def chat(request):
    user_message = request.data.get("message", "")
    requested_model = request.data.get("model", "openrouter/free")
    session_id = request.data.get("session_id", str(uuid.uuid4()))
    history = request.data.get("history", [])
    image_data = request.data.get("image", None)

    if not user_message and not image_data:
        return Response({"error": "Message required"}, status=400)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history[-6:]:
        if msg.get("role") in ["user", "assistant"]:
            messages.append({"role": msg["role"], "content": msg["content"]})

    if image_data:
        messages.append({"role": "user", "content": [
            {"type": "text", "text": user_message or "Please analyze this image"},
            {"type": "image_url", "image_url": {"url": image_data}}
        ]})
    else:
        messages.append({"role": "user", "content": user_message})

    models_to_try = [requested_model] + [m for m in FALLBACK_MODELS if m != requested_model]
    ai_reply = None
    used_model = None

    for try_model in models_to_try:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:3000",
                    "X-Title": "CourierBot"
                },
                json={"model": try_model, "messages": messages, "max_tokens": 800},
                timeout=30
            )
            print("TRYING:", try_model, "STATUS:", response.status_code)
            result = response.json()
            if "error" not in result and "choices" in result:
                ai_reply = result["choices"][0]["message"]["content"]
                used_model = try_model
                break
        except Exception as e:
            print("RETRY:", try_model, str(e))
            continue

    if ai_reply is None:
        return Response({"error": "Sab models busy hain. Thori dair mein try karein."}, status=503)

    try:
        conversation, _ = Conversation.objects.get_or_create(
            session_id=session_id,
            defaults={"model_used": used_model, "title": user_message[:50] if user_message else "Image Chat"}
        )
        Message.objects.create(conversation=conversation, role="user", content=user_message or "Image sent")
        Message.objects.create(conversation=conversation, role="assistant", content=ai_reply)
    except Exception as e:
        print("DB ERROR:", str(e))

    return Response({"reply": ai_reply, "session_id": session_id, "model_used": used_model})


@api_view(["GET"])
def get_history(request, session_id):
    try:
        conversation = Conversation.objects.get(session_id=session_id)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
    except Conversation.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(["GET"])
def list_conversations(request):
    conversations = Conversation.objects.all().order_by("-created_at")[:50]
    result = []
    for c in conversations:
        first_msg = c.messages.filter(role="user").first()
        result.append({
            "session_id": c.session_id,
            "title": (first_msg.content[:40] + "...") if first_msg and len(first_msg.content) > 40 else (first_msg.content if first_msg else "New Chat"),
            "created_at": c.created_at.strftime("%d %b, %I:%M %p"),
        })
    return Response(result)


@api_view(["DELETE"])
def delete_conversation(request, session_id):
    try:
        conversation = Conversation.objects.get(session_id=session_id)
        conversation.delete()
        return Response({"success": True})
    except Conversation.DoesNotExist:
        return Response({"error": "Not found"}, status=404)


@api_view(["GET"])
def get_stats(request):
    total_convos = Conversation.objects.count()
    total_messages = Message.objects.filter(role="user").count()
    favorites = Message.objects.filter(is_favorite=True).count()
    return Response({
        "total_conversations": total_convos,
        "total_messages": total_messages,
        "favorites": favorites,
    })
