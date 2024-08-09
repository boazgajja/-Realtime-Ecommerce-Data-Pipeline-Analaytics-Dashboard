import psycopg2

# Database configuration
DB_HOST = 'project2.czq46i0iwlfj.us-east-1.rds.amazonaws.com'
DB_NAME = 'finalproject'
DB_USER = 'postgres'
DB_PASS = 'boaz0099'

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.products = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, category, product_id):
        node = self.root
        for char in category:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.products.append(product_id)

    def search(self, category):
        node = self.root
        for char in category:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.products if node.is_end_of_word else []

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASS
)
cursor = conn.cursor()

# Fetch product categories and insert into Trie
cursor.execute("SELECT category, product_id FROM products")
products = cursor.fetchall()

trie = Trie()
for category, product_id in products:
    trie.insert(category, product_id)

# Example: Search for products in a category
category_to_search = 'home'  # Example category, adjust as needed
products_in_category = trie.search(category_to_search)
print(f"Products in category '{category_to_search}': {products_in_category}")

cursor.close()
conn.close()
