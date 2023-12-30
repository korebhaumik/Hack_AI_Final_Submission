from uagents import Bureau
from agents.customerSupport_agent import main_agent_customer_service, help_agent
from agents.storeInteraction_agent import (
    main_agent_store,
    fetch_all_agent,
    fetch_doc_agent,
    user,
    merchant,
    purchase_info_agent,
)
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

bureau = Bureau()

try:
    # customer support agents
    bureau.add(main_agent_customer_service)
    bureau.add(help_agent)

    # store interactions agents
    bureau.add(main_agent_store)
    bureau.add(fetch_all_agent)
    bureau.add(fetch_doc_agent)
    bureau.add(user)
    bureau.add(merchant)
    bureau.add(purchase_info_agent)

except Exception as e:
    print(e)


if __name__ == "__main__":
    bureau.run()
