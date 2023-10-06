class Render:
    def __init__(self) -> None:
        pass

    async def _quering_mypost(self, posts):
        mypost = {}

        for post in posts:
            mypost[post[0]] = str(post[1])
        
        return mypost
    
    async def query_mypost(self, posts: dict):
        pages = {}
        current_page = 1
        page_items = {}

        for post_id, title in posts.items():
            page_items[post_id] = title
            if len(page_items) == 5:
                pages[current_page] = page_items
                current_page += 1
                page_items = {}

        # Додайте останню сторінку, якщо там залишилися елементи
        if page_items:
            pages[current_page] = page_items

        return pages
    
    async def page(self, dictionary: dict):
        text = ""
        for key, title in dictionary.items():
            text += f"[ {key} ] {title}\n"
        return text
