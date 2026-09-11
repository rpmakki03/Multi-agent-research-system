from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def _extract_content(agent_output) -> str:
    """Safely extracts text content from various LangChain/LangGraph agent invocation outputs."""
    if isinstance(agent_output, dict):
        if "messages" in agent_output and agent_output["messages"]:
            last_msg = agent_output["messages"][-1]
            return getattr(last_msg, "content", str(last_msg))
        if "output" in agent_output:
            return str(agent_output["output"])
    return str(agent_output)

def run_research_pipeline(topic: str) -> dict:

    state = {}

    # search agent working 
    print("\n" + " =" * 50)
    print("Step 1 - Search Agent is gathering web intelligence...")
    print("=" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = _extract_content(search_result)

    print("\nSearch Results:\n", state['search_results'])

    # step 2 - reader agent 
    print("\n" + " =" * 50)
    print("Step 2 - Reader Agent is scraping deep resources...")
    print("=" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })

    state['scraped_content'] = _extract_content(reader_result)

    print("\nscraped content: \n", state['scraped_content'])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)

