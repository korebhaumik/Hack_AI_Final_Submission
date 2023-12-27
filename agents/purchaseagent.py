import datetime
import time
from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
from controllers.newPurchase import newPurchase


class PaymentRequest(Model):
    wallet_address: str
    denom: str
    amount: int
    pricePerBook: int
    quantity: int
    title: str
    address: str


class TransactionInfo(Model):
    tx_hash: str
    wallet_address: str
    amount: int
    pricePerBook: int
    quantity: int
    title: str
    address: str


DENOM = "atestfet"

user = Agent(name="user", seed="user secret phrase")
bank = Agent(name="bank", seed="bank secret phrase")

fund_agent_if_low(user.wallet.address())
fund_agent_if_low(bank.wallet.address())


@bank.on_interval(period=30.0)
async def request_funds(ctx: Context):
    purchase_details = {
        "title": "To Kill a Mockingbird",
        "pricePerBook": 2,
        "quantity": 1,
        "user_walet_address": "fetch146rgrqzxgnwquk6pchxdzrm5al7wxdjwxg6ym7",
        "address": "marol",
    }
    amount = purchase_details["quantity"] * purchase_details["pricePerBook"]
    ctx.logger.info(f"\033[96m TRANSACTION OF {amount} {DENOM} REQUESTED")
    await ctx.send(
        user.address,
        PaymentRequest(
            wallet_address=str(purchase_details["user_walet_address"]),
            denom=DENOM,
            amount=amount,
            pricePerBook=purchase_details["pricePerBook"],
            quantity=purchase_details["quantity"],
            title=purchase_details["title"],
            address=purchase_details["address"],
        ),
    )


@user.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(
        f"\033[96m RECIEVED PAYMENT REQUEST FROM {sender} FOR {msg.amount} {DENOM}"
    )
    transaction = ctx.ledger.send_tokens(
        msg.wallet_address, msg.amount, msg.denom, ctx.wallet
    )
    await ctx.send(
        bank.address,
        TransactionInfo(
            tx_hash=transaction.tx_hash,
            wallet_address=msg.wallet_address,
            amount=msg.quantity * msg.pricePerBook,
            pricePerBook=msg.pricePerBook,
            quantity=msg.quantity,
            title=msg.title,
            address=msg.address,
        ),
    )


@bank.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"\033[96m PROCESSING TRANSACTION_HASH {msg.tx_hash}")
    tx_resp = await wait_for_tx_to_complete(ledger=ctx.ledger, tx_hash=msg.tx_hash)
    coin_received = tx_resp.events["coin_received"]
    currentDate = datetime.datetime.now()
    if (
        coin_received["receiver"] == str(msg.wallet_address)
        and coin_received["amount"] == f"{msg.amount}{DENOM}"
    ):
        ctx.logger.info(
            f"\033[96m TRANSACTION OF {coin_received} {DENOM} SUCCESSFULL. from {msg.wallet_address} -> BANK"
        )
        foo = newPurchase(
            title=msg.title,
            pricePerBook=msg.pricePerBook,
            quantity=msg.quantity,
            walet_address=msg.wallet_address,
            datetime=str(currentDate),
            delivery_date=str(currentDate + datetime.timedelta(days=2)),
            delivery_address=msg.address,
        )
        if foo:
            ctx.logger.info(f"\033[96m TRANSACTION RECORDED IN DATABASE")
        else:
            ctx.logger.info(f"Failed while putting in Database")


# bureau = Bureau()
# bureau.add(user)
# bureau.add(bank)

# if __name__ == "__main__":
#     bureau.run()