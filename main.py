from aijson import Flow, RedisCacheRepo
import asyncio
import my_actions
from dotenv import load_dotenv
import glob
import os

def get_latest_directory(document_folder='documents'):
    existing_folders = glob.glob(os.path.join(document_folder, '*'))
    existing_numbers = [int(os.path.basename(folder)) for folder in existing_folders if os.path.basename(folder).isdigit()]
    if not existing_numbers:
        return None
    latest_folder = str(max(existing_numbers))
    return os.path.join(document_folder, latest_folder)

# load environment variables from .env
load_dotenv()

async def main():
    # Get the latest directory
    latest_directory = get_latest_directory()

    if latest_directory is None:
        print("No directories found.")
        return

    # Load PDFs from the latest directory
    recipes_glob = os.path.join(latest_directory, "*.pdf")
    document_paths = glob.glob(recipes_glob)
    print("Reading the following PDFs:", document_paths)
    if not document_paths:
        print(f"No PDFs found in {latest_directory}.")
        return
    
    # load the flow
    flow = Flow.from_file(
        'omniAns.ai.yaml',
        cache_repo=RedisCacheRepo
    ).set_vars(
        pdf_filepaths=document_paths,
    )

    # set any variables
    message = "Comparing Lydia Goehr's explanation of 'The Beethoven Paradigm' of musical works to Nicholas Cook's in 'The Other Beethoven'."
    flow = flow.set_vars(message=message)

    # run it
    result = await flow.run()
    
    
    print(result)

    # # alternatively, INSTEAD of running it, stream it
    # async for result in flow.stream():
    #     print(result)

if __name__ == '__main__':
    asyncio.run(main())