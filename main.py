import glob
import os
from pathlib import Path

from asyncflows import AsyncFlows

def get_latest_directory(document_folder='documents'):
    existing_folders = glob.glob(os.path.join(document_folder, '*'))
    existing_numbers = [int(os.path.basename(folder)) for folder in existing_folders if os.path.basename(folder).isdigit()]
    if not existing_numbers:
        return None
    latest_folder = str(max(existing_numbers))
    return os.path.join(document_folder, latest_folder)

async def main():
    # Get the latest directory
    latest_directory = get_latest_directory()
    if latest_directory is None:
        print("No directories found.")
        return

    # Load PDFs from the latest directory
    recipes_glob = os.path.join(latest_directory, "*.pdf")
    document_paths = glob.glob(recipes_glob)
    if not document_paths:
        print(f"No PDFs found in {latest_directory}.")
        return

    # Load the chatbot flow
    flow = AsyncFlows.from_file("omniAns.yaml").set_vars(
        pdf_filepaths=document_paths,
    )

    # Get the user's query via CLI interface
    try:
        message = input("What's your essay question: ")
    except EOFError:
        return

    # Set the query and run the flow
    query_flow = flow.set_vars(message=message)
    result = await query_flow.run()
    print(result)

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())



    