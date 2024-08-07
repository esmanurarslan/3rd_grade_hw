from graphviz import Digraph

class Node:
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf
        self.keys = []
        self.ptrs = []
        self.data = []  # To store plaintiff and defendant data in leaf nodes
        self.next = None  # Pointer to the next leaf node
        self.prev = None  # Pointer to the previous leaf node

class BTree:
    def __init__(self, bucket_size=3):
        self.root = None
        self.bucket_size = bucket_size

    def insert(self, key, plaintiff=None, defendant=None):
        if not self.root:
            self.root = Node()
            self.root.keys.append(key)
            self.root.data.append((plaintiff, defendant))
            self.root.is_leaf = True
            return

        current = self.root
        parent = None

        while not current.is_leaf:
            parent = current

            for i in range(len(current.keys)):
                if key < current.keys[i]:
                    current = current.ptrs[i]
                    break

                if i == len(current.keys) - 1:
                    current = current.ptrs[i + 1]
                    break

        if len(current.keys) < self.bucket_size:
            i = 0
            while i < len(current.keys) and key > current.keys[i]:
                i += 1

            current.keys.insert(i, key)
            current.data.insert(i, (plaintiff, defendant))
            current.ptrs.append(None)
        else:
            new_leaf = Node()
            new_leaf.is_leaf = True
            temp_keys = current.keys[:]
            temp_data = current.data[:]
            i = 0

            while i < self.bucket_size and key > temp_keys[i]:
                i += 1

            temp_keys.insert(i, key)
            temp_data.insert(i, (plaintiff, defendant))
            mid = len(temp_keys) // 2

            current.keys = temp_keys[:mid]
            current.data = temp_data[:mid]
            new_leaf.keys = temp_keys[mid:]
            new_leaf.data = temp_data[mid:]

            # Link the new leaf node with the current leaf node
            new_leaf.next = current.next
            if new_leaf.next:
                new_leaf.next.prev = new_leaf
            current.next = new_leaf
            new_leaf.prev = current

            if current == self.root:
                new_root = Node(is_leaf=False)
                new_root.keys.append(new_leaf.keys[0])
                new_root.ptrs.append(current)
                new_root.ptrs.append(new_leaf)
                self.root = new_root
            else:
                self.shift_level(new_leaf.keys[0], parent, new_leaf)

    def shift_level(self, x, current, child):
        if len(current.keys) < self.bucket_size:
            i = 0
            while i < len(current.keys) and x > current.keys[i]:
                i += 1

            current.keys.insert(i, x)
            current.ptrs.insert(i + 1, child)
        else:
            new_internal = Node(is_leaf=False)
            temp_keys = current.keys[:]
            temp_ptrs = current.ptrs[:]
            i = 0

            while i < len(temp_keys) and x > temp_keys[i]:
                i += 1

            temp_keys.insert(i, x)
            temp_ptrs.insert(i + 1, child)

            mid = len(temp_keys) // 2

            current.keys = temp_keys[:mid]
            new_internal.keys = temp_keys[mid + 1:]

            current.ptrs = temp_ptrs[:mid + 1]
            new_internal.ptrs = temp_ptrs[mid + 1:]

            if current == self.root:
                new_root = Node(is_leaf=False)
                new_root.keys.append(temp_keys[mid])
                new_root.ptrs.append(current)
                new_root.ptrs.append(new_internal)
                self.root = new_root
            else:
                self.shift_level(temp_keys[mid], self.find_parent(self.root, current), new_internal)

    def find_parent(self, current, child):
        if current.is_leaf or current.ptrs[0].is_leaf:
            return None

        for i in range(len(current.ptrs)):
            if current.ptrs[i] == child:
                return current
            else:
                parent = self.find_parent(current.ptrs[i], child)
                if parent:
                    return parent

    def search(self, key):
        if not self.root:
            return -1, None
        else:
            current = self.root
            while not current.is_leaf:
                for i in range(len(current.keys)):
                    if key < current.keys[i]:
                        current = current.ptrs[i]
                        break
                    if i == len(current.keys) - 1:
                        current = current.ptrs[i + 1]
                        break

            for i, k in enumerate(current.keys):
                if k == key:
                    return 1, current.data[i]
            return 0, None

    def display(self, current):
        if not current:
            return

        queue = [current]
        while queue:
            length = len(queue)

            for _ in range(length):
                t_node = queue.pop(0)

                for i in range(len(t_node.keys)):
                    if t_node.is_leaf:
                        print(f"{t_node.keys[i]} ({t_node.data[i][0]}, {t_node.data[i][1]})", end=" ")
                    else:
                        print(t_node.keys[i], end=" ")

                for ptr in t_node.ptrs:
                    if ptr:
                        queue.append(ptr)

                print("\t", end="")
            print()

    def find_nth_element(self, n):
        if not self.root:
            return None

        current = self.root
        while not current.is_leaf:
            current = current.ptrs[0]

        count = 0
        while current:
            for i in range(len(current.keys)):
                if count == n:
                    return current.keys[i], current.data[i]
                count += 1
            current = current.next

        return None

    def visualize(self):
        if not self.root:
            return "Tree is empty"
        
        dot = Digraph()
        self._visualize(self.root, dot)
        dot.render("bplus_tree", format="png", cleanup=True)
        return dot

    def _visualize(self, node, dot, parent=None, edge_label=""):
        node_id = str(id(node))
        label = '|'.join(map(str, node.keys))
        dot.node(node_id, label=label)
        
        if parent:
            dot.edge(parent, node_id, label=edge_label)
        
        for i, child in enumerate(node.ptrs):
            if child:
                self._visualize(child, dot, node_id, str(i))

def create_bplus_tree_from_file(filename, bucket_size=3):
    tree = BTree(bucket_size)
    i = 0
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split('|')
            key = int(parts[0])
            plaintiff = str(parts[1])
            defendant = str(parts[2])
            tree.insert(key, plaintiff, defendant)
            i += 1
            if i > 20:
                break

    return tree

if __name__ == "__main__":
    tree = create_bplus_tree_from_file("//Users/esmanurarslan/Library/Mobile Documents/com~apple~CloudDocs/6th term/File Organization/BMI3241_EsmaNur-Arslan-A1/code/record.dat", 3)
    
    # Search for a specific key
    key_to_search = 76783  # Change this to the key you want to search for
    found, data = tree.search(key_to_search)
    if found:
        print(f"Key {key_to_search} found with plaintiff: {data[0]}, defendant: {data[1]}")
    else:
        print(f"Key {key_to_search} not found in the tree.")

    # Display the B+ tree
    print("\nB+ Tree structure:")
    tree.display(tree.root)

    # Find the 10th element in the leaf nodes
    n = 10  # Change this to the element index you want to find
    nth_element = tree.find_nth_element(n-1)
    if nth_element:
        print(f"\nThe {n}th element is key: {nth_element[0]}, plaintiff: {nth_element[1][0]}, defendant: {nth_element[1][1]}")
    else:
        print(f"\nThe {n}th element does not exist.")
    
    # Visualize the B+ tree
    dot = tree.visualize()
    print("B+ tree visualized and saved as bplus_tree.png")