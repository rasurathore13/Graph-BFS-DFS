import re
import random

class vertex():
    def __init__(self, key):
        self.id = key
        self.connected_to = {}
    
    def add_neighbours(self, neighbour, weight = 0):
        self.connected_to[neighbour] = weight
    
    def get_id(self):
        return self.id
    
    def get_neighbours(self):
        return self.connected_to.keys()

class graph():
    def __init__(self):
        self.vertices = {}
    
    def add_vertex(self, vertex_key):
        self.vertices[vertex_key] = vertex(vertex_key)

    def add_edge(self, first_key, second_key, weight = 0):
        if first_key not in self.vertices.keys():
            self.vertices[first_key] = vertex(first_key)
        if second_key not in self.vertices.keys():
            self.vertices[second_key] = vertex(second_key)
        self.vertices[first_key].add_neighbours(self.vertices[second_key], weight)
        self.vertices[second_key].add_neighbours(self.vertices[first_key], weight)
    
    def get_vertices_list(self):
        return self.vertices.keys()

    def get_vertex(self, vertex_key):
        return self.vertices[vertex_key]

def breadth_first_search(g, first_key, target_key):
    visited = {}
    return_lst = [first_key]
    for i in g.get_vertices_list():
        visited[i] = 0
    queue = [first_key]
    visited[first_key] = 1
    parents = [[first_key,None]]
    while len(queue) != 0:
        s = queue[0]
        flag = False
        queue = queue[1:]
        for i in [j.get_id() for j in g.get_vertex(s).get_neighbours()]:
            if visited[i] == 0:
                visited[i] = 1
                queue.append(i)
                if i == target_key:
                    parents.append([i,s])
                    flag = True
                    break
                else:
                    parents.append([i, s])
        if flag:
            lst = []
            temp = parents[-1]
            while temp[1] != None:
                lst.append(temp[0])
                for i in parents:
                    if i[0] == temp[1]:
                        temp = i
                        break
            lst.append(temp[0])
            return lst[::-1]
        return None


def depth_first_search(g, first_key, second_key):
    visited = {}
    for i in g.get_vertices_list():
        visited[i] = 0
    stack =[first_key]
    visited[first_key] = 1
    while len(stack) != 0:
        if stack[-1] == second_key:
            return stack
        for i in [i.get_id() for i in g.get_vertex(stack[-1]).get_neighbours()]:
            if visited[i] == 0:
                visited[i] = 1
                stack.append(i)
                break
        else:
            stack = stack[:-1]

if __name__ == '__main__':
    global word_array
    with open('text_for_word_ladder_problem.txt', 'r') as file:
        file_text = file.read()
        word_array = re.findall(r"\w{4}", file_text.strip('\n'))
        lst = ['FOOL', 'POOL','POLL','POLE','PALE','SALE','SAGE']
        new_lst = []
        while len(new_lst) <= len(lst):
            a = random.randint(0,len(word_array)-1)
            if a not in new_lst:
                new_lst.append(a)
        for i in range(len(lst)):
            word_array[new_lst[i]] = lst[i]
        print(new_lst)
        
    g = graph()
    bucket_list = {}
    for i in word_array:
        if type(i) == type(int): print(i)
        g.add_vertex(i)
        for j in range(len(i)):
            bucket = i[:j]+'_'+i[j+1:]
            try:
                bucket_list[bucket].append(i)
            except KeyError:
                bucket_list[bucket] = [i]
    for i in bucket_list.keys():
        for j in range(len(bucket_list[i])):
            for k in range(j+1, len(bucket_list[i])):
                g.add_edge(bucket_list[i][j], bucket_list[i][k])
    print(breadth_first_search(g, 'FOOL', 'SAGE'))
    
    