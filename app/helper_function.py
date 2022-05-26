def format_tags(results):
    for item in results:
        item["tags"] = list(map(lambda x: x["tag_text"], item["tags"]))
        # item["tags"] = [ item["tags"]['tag_text'] for a in item["tags"]]

    return results

