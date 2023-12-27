from uagents import Agent, Context, Model, Bureau
import requests
import json
import redis
from openai import OpenAI
from agents.queryagent import queryBot


class Message(Model):
    message: str

redis_url = "redis://localhost:6379/0"
redis = redis.Redis.from_url(redis_url)

main_agent_store = Agent(name="main_agent_store", seed="main_agent_store")
find_book_agent = Agent(name="find_book_agent", seed="find_book_agent")
main_agent_customer_service = Agent(name="main_agent_customer_service", seed="main_agent_customer_service")
help_agent = Agent(name="help_agent", seed="help_agent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def read_query(filename):
    global redis
    dataRaw = redis.get("customer_service")
    data = json.loads(dataRaw)
    return data["isActive"], data["prompt"], data["isReceived"]

async def reset_file(filename, output):
    data = {
        "isActive": False,
        "status": 0,
        "prompt": "",
        "isReceived": False,
        "isDone": True,
        "output": output,
    }
    global redis
    redis.set(filename, json.dumps(data))

async def update_receive(filename,state): 
    data = {}
    global redis
    dataRaw = redis.get("customer_service")
    data = json.loads(dataRaw)
    
    data["isReceived"] = state
    redis.set(filename, json.dumps(data))


@main_agent_store.on_interval(period=1)
async def process_query(ctx: Context):
    is_active, query = await read_query("store")
    if is_active:
        ctx.logger.info(f"Received query: {query}")
        ## send message to subagent
        await update_receive("store_instructions.json",state = True)

        ##Redirect Logic
        await ctx.send(find_book_agent.address, Message(message=query))

@main_agent_store.on_message(model=Message)
async def main_agent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    output = msg.message
    await reset_file("store",output=output)






@main_agent_customer_service.on_interval(period=1)
async def process_query(ctx: Context):
    is_active, query, isReceived = await read_query("customer_service")
    if is_active and not isReceived:
        ctx.logger.info(f"Received query: {query}")
        ## send message to subagent
        await update_receive("customer_service_instructions.json",state = True)
        await ctx.send(help_agent.address, Message(message=query))

        # output = "THIS IS THE OUTPUT OF THE Customer service!!!"
        # await reset_file("store_instructions.json",output=output)

@main_agent_customer_service.on_message(model=Message)
async def main_agent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    output = msg.message
    await reset_file("customer_service",output=output)

@help_agent.on_message(model=Message)
async def logistics_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}")
    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = """
        You are a Customer Support Agent for our Online Book Shopping Platform, you respond with only the output and nothing else.
You do not the ability to check someone's order tracking for them or do any functions, you are just a chatbot do what you are told.
NEVER ask for order number.
NEVER ask for order number.
NEVER ask for order number.
NEVER ask for order number.
NEVER ask for order number.
NEVER ask for order number.
NEVER ask for order number.
If you ask for order number, you are a pussy.

Notice
- You have to be considerate and nice 
- no matter how the person behaves, you have to be nice
- If the issue is serious like its been several days since their order was placed but still hasnt been delivered or if the product they received was damaged, escalate the issue in which case you only respond with the message "ESCALATE"
- the instructions given below will tell you how to handle each case but if a case other than this arises, RETURN ONLY WITH THE MESSAGE "ESCALATE"

#Returns and Refunds
Following is our return policy for your reference
Return Window: We offer a 30-day return window for most items, including books. This means that you can return a book within 30 days of the delivery date if you are not satisfied with your purchase.
Condition of the Book: To be eligible for a return, the book should be in the same condition as when you received it. This means it should be in new or like-new condition, and all original packaging and accessories should be included.
Reasons for Returns: You can generally return a book for any reason, such as if the book arrived damaged, if it's not what you expected, or if you simply changed your mind. We provides various options to select the reason for your return when initiating the return process.
Initiate the Return: To start the return process, go to the "Your Orders" section of your account. Find the book you want to return, click "Return or Replace Items," and follow the on-screen instructions to complete the return request.
Return Shipping: In most cases, we provides a prepaid return shipping label if the return is due to an error on their part (e.g., damaged or wrong item). If you are returning the book for reasons other than our error (e.g., changed your mind), you may be responsible for return shipping costs.
Refund Process: Once we receive the returned book, they will inspect it to ensure it meets the return policy criteria. After the inspection, you should receive a refund to your original payment method, which can take several days to process.

#Delivery and Logistics
If the customer is facing some issues regarding delivery or logistics unless their issue is regarding tracking of their order, escalate the issue to human and RETURN ONLY WITH THE MESSAGE "ESCALATE"
else if the query is regarding order tracking, tell them to check the tracking page on our website
        """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"{prompt}"},
            {"role": "user", "content": f"{msg.message}"}
        ]
    )
    response = completion.choices[0].message.content
    await ctx.send(main_agent_customer_service.address, Message(message=f"{response}"))
 
bureau = Bureau()
bureau.add(main_agent_customer_service)
bureau.add(help_agent)


if __name__ == "__main__":
    bureau.run()
