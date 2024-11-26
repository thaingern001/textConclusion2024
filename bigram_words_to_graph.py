import ast

# Open the file and read the content
with open("log/log004.txt") as f: #<============= path of cleaned data here
    # Read the file content as a string
    content = f.read()
    
    # Use ast.literal_eval to safely parse the string representation into a Python list
    data = ast.literal_eval(content)
# print(content)


class Node_bigram:
    def __init__ (self,bigram_word):
        self.bigram_word = bigram_word
        self.bigram_pair = bigram_word.split()
        self.next = {} #key = bigram_word,value = Node_bigram
        self.prev = {}
        self.n_edge_next = 0
        self.n_edge_prev = 0
    def add_prev(self,prev):
        self.n_edge_prev+=1
        for i in self.prev:
            if i == prev.bigram_word:
                # print("9999999999999999999999999999999999")
                self.prev[i][1] +=1
                return
        self.prev[prev.bigram_word] = [prev,1]
    def add_next(self,next):
        self.n_edge_next+=1
        for i in self.next:
            if i == next.bigram_word:
                # print("9999999999999999999999999999999999")
                self.next[i][1] +=1
                return
        self.next[next.bigram_word] = [next,1]

class Graph:
    def __init__(self):
        self.vertices = {} #key = bigram_word,value = Node_bigram
        self.edges = {} 
    def add_node(self,node):
        for i in self.vertices:
            if node.bigram_word == i:
                # print("***************foud duplicate")
                return
        self.vertices[node.bigram_word] = node

        
def add_text_to_vertice_of_graph(g,text):
    for i in range(len(text)):
        now_node = Node_bigram(text[i])
        g.add_node(now_node)

def make_adge(g,text):
    for i in range(len(text)): 
        if i == 0: #first bigram of text
            # print("case1")
            now_node = g.vertices[text[i]]
            # next_node = Node_bigram(text[i+1])
            next_node = g.vertices[text[i+1]]
            now_node.add_next(next_node)
            # g.add_node(now_node)
            continue
        elif i == len(text)-1: #last of bigram in text
            # print("case3")
            # prev_node = Node_bigram(text[i-1])
            prev_node = g.vertices[text[i-1]]
            now_node = g.vertices[text[i]]
            now_node.add_prev(prev_node)
            # g.add_node(now_node)
            continue
        else :
            # print("case2")
            prev_node = g.vertices[text[i-1]]
            now_node = g.vertices[text[i]]
            next_node = g.vertices[text[i+1]]
            now_node.add_next(next_node)
            now_node.add_prev(prev_node)
            # g.add_node(now_node)
            continue

def add_text_to_graph(g,text):
    if len(text) <= 1 :     
        add_text_to_vertice_of_graph(g,text)
        return
    add_text_to_vertice_of_graph(g,text)
    make_adge(g,text)

def CleanData_to_graph(data,graph):
    for text in data:
        add_text_to_graph(graph,text)



#test only 1 text from data
# n = 54
# text = data[n]
# # text = text+data[1]
# # text = text+data[1]+data[2]+data[3]+data[3]
# print("index is",n,f"text is : {text}")
#add every bigram in text to be vertice in graph

g = Graph() #make grap for restore data

CleanData_to_graph(data,g)

# for i in g.vertices:
#     w = g.vertices[i]
#     # print(g.vertices[i].bigram_word,)
#     print(w.bigram_word,w.prev)
#     # print(i)





#----------------------------------------more about fist word of conclusion----------------------------
print(len(g.vertices))
def find_first_words(g):
    n = 0
    ans = []
    for i in g.vertices:
        if g.vertices[i].n_edge_prev >= n:
            if g.vertices[i].n_edge_prev == n:
                ans.append(i)
            ans = [i]
            n = g.vertices[i].n_edge_prev
    return ans
        
ans = find_first_words(g)
print(ans)
