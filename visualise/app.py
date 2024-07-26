from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from graphviz import Digraph

app = Flask(__name__)

# Ensure the Graphviz binaries are in the PATH
os.environ["PATH"] += os.pathsep + 'C:/Users/Sujank/Desktop/coding/windows_10_cmake_Release_Graphviz-10.0.1-win64/Graphviz-10.0.1-win64/bin'

COUNT = [10]

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None
    
    def buildTree(self, eltlist):
        eltlist=[TreeNode(x) for x in eltlist]
        self.root=eltlist[0]
        for i in range(len(eltlist)):
            if type(eltlist[i].data)==int:
                eltlist[i].left=eltlist[i+1]
                eltlist[i].right=eltlist[i+2]

def add_edges(dot, node):
    if node.left:
        dot.edge(str(node.data), str(node.left.data))
        add_edges(dot, node.left)
    if node.right:
        dot.edge(str(node.data), str(node.right.data))
        add_edges(dot, node.right)

def visualize_tree(tree):
    dot = Digraph(comment='Binary Tree')
    if tree.root:
        dot.node(str(tree.root.data))
        add_edges(dot, tree.root)
    dot.render('binary_tree', format='png', view=True)

def func(blocks):
    sorted_blocks = sorted(blocks, key=lambda x: x[1] - x[0], reverse=True)
    differences = [abs(block[1] - block[0]) + 1 for block in sorted_blocks]
    cumulative_sums = [sum(differences[i:]) for i in range(len(differences))]
    alternating_list = []
    for i in range(len(cumulative_sums)):
        alternating_list.append(cumulative_sums[i])
        if i < len(sorted_blocks):
            alternating_list.append(sorted_blocks[i])
    alternating_list.pop(len(alternating_list)-2)
    return alternating_list


class MemoryAllocator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.free_blocks = [(0, total_memory - 1)]
        self.allocated_blocks = []

    def allocate(self, size):
        index = self.find_block(size)

        if index == -1:
            return (-1, -1)

        while (self.free_blocks[index][1] - self.free_blocks[index][0] + 1) > size and \
                (self.free_blocks[index][1] - self.free_blocks[index][0] + 1) // 2 >= size:
            self.split_block(index)

        allocated_block = self.free_blocks[index]
        del self.free_blocks[index]
        self.allocated_blocks.append(allocated_block)
        return allocated_block

    def free(self, ind):
        block = self.find_block_to_free(ind)
        if block[0] == -1:
            return

        for i in range(len(self.free_blocks)):
            if block[1] < self.free_blocks[i][0]:
                self.free_blocks.insert(i, block)
                self.allocated_blocks.remove(block)
                break

        while self.merge_with_buddy(i):
            continue

    def find_block(self, size):
        for i in range(len(self.free_blocks)):
            if (self.free_blocks[i][1] - self.free_blocks[i][0] + 1) >= size:
                return i
        return -1

    def split_block(self, index):
        start, end = self.free_blocks[index]
        block_size = (end - start + 1) // 2
        self.free_blocks[index] = (start, start + block_size - 1)
        self.free_blocks.insert(index + 1, (start + block_size, end))

    def merge_with_buddy(self, index):
        buddy_index = index + 1 if index % 2 == 0 else index - 1
        if buddy_index < len(self.free_blocks) and \
                self.free_blocks[index][1] - self.free_blocks[index][0] + 1 == \
                self.free_blocks[buddy_index][1] - self.free_blocks[buddy_index][0] + 1:
            self.free_blocks[index] = (self.free_blocks[index][0], self.free_blocks[buddy_index][1])
            del self.free_blocks[buddy_index]
            return True
        return False

    def find_block_to_free(self, ind):
        for block in self.allocated_blocks:
            if block[0] == ind:
                return block
        return (-1, -1)

    def get_free_blocks(self):
        return self.free_blocks

    def get_allocated_blocks(self):
        return self.allocated_blocks

allocator = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initialize', methods=['POST'])
def initialize():
    global allocator
    total_memory = int(request.form['total_memory'])
    allocator = MemoryAllocator(total_memory)
    return redirect(url_for('index'))

@app.route('/allocate', methods=['POST'])
def allocate():
    global allocator
    size = int(request.form['size'])
    allocated_block = allocator.allocate(size)
    l = allocator.get_free_blocks() + allocator.get_allocated_blocks()
    l = func(l)
    myTree = Tree()
    myTree.buildTree(l)
    visualize_tree(myTree)
    return redirect(url_for('index'))

@app.route('/free', methods=['POST'])
def free():
    global allocator
    index = int(request.form['index'])
    allocator.free(index)
    l = allocator.get_free_blocks() + allocator.get_allocated_blocks()
    l = func(l)
    myTree = Tree()
    myTree.buildTree(l)
    visualize_tree(myTree)
    return redirect(url_for('index'))

@app.route('/image')
def image():
    return send_file('static/binary_tree.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
