import ast

# Open the file and read the content
with open("log/log003.txt") as f: #<============= path of cleaned data here
    # Read the file content as a string
    content = f.read()
    
    # Use ast.literal_eval to safely parse the string representation into a Python list
    data = ast.literal_eval(content)
# print(content)


class Node_bigram:
    def __init__ (self,bigram_word):
        self.bigram_word = bigram_word
        self.index = 0
        self.bigram_pair = bigram_word.split()
        self.next = {} #key = bigram_word,value = [Node_bigram , weight]
        self.prev = {} #key = bigram_word,value = [Node_bigram , weight]
        self.n_edge_next = 0
        self.n_edge_prev = 0
        self.rank_point = 0

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

# class Graph:
#     def __init__(self):
#         self.vertices = {} #key = bigram_word,value = Node_bigram
#         self.edges = {} 
#     def add_node(self,node):
#         for i in self.vertices:
#             if node.bigram_word == i:
#                 # print("***************foud duplicate")
#                 return
#         node.index = len(self.vertices)
#         self.vertices[node.bigram_word] = node
#     def ranking(self,n_time):
#         alpha = 0.85

#         vertices_num = len(self.vertices)
#         #give RP from Rank_Point
#         start_RP = [(1-alpha)/vertices_num]*vertices_num
#         # next_RP = [0]*vertices_num
#         nodes = list(self.vertices.values()) #==> [node_bigram,w]
#         # print(nodes[0].next)
#         def calculate(start_RP,nodes):  
#             next_RP = [(1-alpha)/vertices_num]*vertices_num
#             for i in range(len(nodes)):
#                 # print("node2 = ",nodes[2])
#                 # return
#                 node = nodes[i]
#                 # w = nodes[i][1] #fequency
#                 rp = start_RP[i] #rank point of this node
#                 if node.n_edge_next == 0 :
#                     rp_per_adge = rp/vertices_num
#                     for j in range(len(start_RP)):
#                         next_RP[j]+=rp_per_adge
#                     continue
#                 rp_per_adge = rp/node.n_edge_next 
#                 for next in node.next.values():
#                     # print(next)
#                     # print(next[0])
#                     # print(next[1])
#                     next_node = next[0]
#                     w = next[1]
#                     # print(rp_per_adge*w)
#                     next_RP[next_node.index] += rp_per_adge*w*alpha
#                     # return
#             return next_RP
#         now = start_RP
#         for i in range(n_time):
#             now = calculate(now,nodes)
#             print("test:",now[:3])
#             print("sum = " ,sum(now))
#             print(f"n = {i+1} complete")
#         # now = calculate(start_RP,nodes)
#         print(now[:3])
#         print("len = ",len(now))
#         print("max = " ,max(now))
#         print("sum = " ,sum(now))


class Graph:
    def __init__(self):
        self.vertices = {}  # Key = bigram_word, value = Node_bigram
        self.edges = {}

    def add_node(self, node):
        for i in self.vertices:
            if node.bigram_word == i:
                return
        node.index = len(self.vertices)
        self.vertices[node.bigram_word] = node

    def ranking(self, n_time):
        alpha = 0.85
        vertices_num = len(self.vertices)

        # Initialize rank points with the damping factor
        start_RP = [(1 - alpha) / vertices_num] * vertices_num
        nodes = list(self.vertices.values())

        def calculate(start_RP, nodes):
            next_RP = [(1 - alpha) / vertices_num] * vertices_num
            dangling_sum = 0  # Accumulate rank points for dangling nodes

            for i in range(len(nodes)):
                node = nodes[i]
                rp = start_RP[i]

                if node.n_edge_next == 0:  # Handle dangling nodes
                    dangling_sum += rp
                    continue

                rp_per_edge = rp / node.n_edge_next
                for next in node.next.values():
                    next_node = next[0]
                    w = next[1]
                    next_RP[next_node.index] += rp_per_edge * w * alpha

            # Redistribute dangling rank points uniformly
            for j in range(vertices_num):
                next_RP[j] += dangling_sum * alpha / vertices_num

            # Normalize to ensure the sum of rank points equals 1
            total_sum = sum(next_RP)
            next_RP = [rp / total_sum for rp in next_RP]

            return next_RP

        now = start_RP
        for i in range(n_time):
            now = calculate(now, nodes)
            print(f"Iteration {i + 1}: Top 3 RPs = {now[:3]}, Sum = {sum(now):.6f}")

        # print("Final Rank Points:", now[:3])
        # print("Total Sum:", sum(now))
        for i in range(vertices_num):
            nodes[i].rank_point = now[i]
        return now
    def printRank(self,n):
        vertices_sorted = sorted(self.vertices, key=lambda k: self.vertices[k].rank_point,reverse=True)
        # for i in range(n):
        #     bi_word = vertices_sorted[i]
            # rp = self.
            # print()
        return vertices_sorted
#0.005974815658156412
#0.005974815658156412
#0.005974815658156412


        
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

g = Graph() #make grap for restore data

CleanData_to_graph(data,g)


#---------------------------------------- finish make graph G ----------------------------

# num_of_verices = len(g.vertices)

# for i in g.vertices:
#     w = g.vertices[i]
#     # print(g.vertices[i].bigram_word,)
#     print(w.bigram_word,w.prev)
#     # print(i)

print(max(g.ranking(100)))
print(g.printRank(1)[:10])





#----------------------------------------more about fist word of conclusion----------------------------
print(len(g.vertices))
# def find_first_words(g):
#     n = 0
#     ans = []
#     for i in g.vertices:
#         if g.vertices[i].n_edge_prev >= n:
#             if g.vertices[i].n_edge_prev == n:
#                 ans.append(i)
#             ans = [i]
#             n = g.vertices[i].n_edge_prev
#     return ans
        
# ans = find_first_words(g)
# print(ans)
