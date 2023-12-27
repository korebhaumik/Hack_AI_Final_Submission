from uagents import Agent, Bureau, Context, Model
from controllers.queryBooks import query_books
from typing import Optional, List

queryBot = Agent(name="queryBot", seed="alice recovery phrase")
customer = Agent(name="customer", seed="korebhaumik")


class Message(Model):
    action: str
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None  # Changed from Tuple to float
    quantity: Optional[int] = None
    rating: Optional[float] = None
    tags: Optional[List[str]] = None  # Changed from str to List[str]


@queryBot.on_event("startup")
async def say_hello(ctx: Context):
    print("QUERYBOT agent running address: ", ctx.address)


@customer.on_event("startup")
async def say_hello(ctx: Context):
    print("CUSTOMER agent running address: ", ctx.address)


# @customer.on_interval(period=10.0)
# async def say_hello(ctx: Context):
#     print("My name is bhaumik")


# @customer.on_interval(period=10.0)
# async def sendRequest(ctx: Context):
#     ctx.logger.info("\033[96m Requesting Book with Title: To Kill a Mockingbird")
#     await ctx.send(
#         queryBot.address, Message(action="request", title="To Kill a Mockingbird")
#     )


@queryBot.on_message(model=Message)
async def handleRequest(ctx: Context, sender: str, msg: Message):
    if msg.action == "request":
        ctx.logger.info(f"\033[96m Received Query for {msg}")
        queryResult = query_books(
            title=msg.title,
            # description=msg.description,
            # price=msg.price,
            # quantity=msg.quantity,
            # rating=msg.rating,
            # tags=msg.tags,
        )
        if queryResult:
            bookList = queryResult.get("documents", [])
            print(bookList, " books found in database")
            for book in bookList:
                await ctx.send(
                    customer.address,
                    Message(
                        action="response",
                        title=book["title"],
                        description=book["description"],
                        price=float(book["price"]),
                        quantity=int(book["quantity"]),
                        rating=float(book["rating"]),
                        tags=book["tags"],
                    ),
                )
        else:
            print("No results or error occurred.")


@customer.on_message(model=Message)
async def handleResponse(ctx: Context, sender: str, msg: Message):
    print("message recieved")
    if msg.action == "response":
        ctx.logger.info(f"\033[96m Got Response from QueryBot {msg}")


# bureau = Bureau()
# bureau.add(queryBot)
# bureau.add(customer)

# if __name__ == "__main__":
#     print("starting")
#     bureau.run()