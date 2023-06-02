# Ejercicio 25
class Employee:
    def __init__(self, id, fun):
        self.id = id
        self.fun = fun
        self.children = []
        self.left = None
        self.right = None

def max_fun_party(root):
    if not root:
        return (0, 0)
    # Caso base: no hay empleados
    if not root.children:
        return (0, root.fun)
    # Caso base: solo hay un empleado
    if len(root.children) == 1:
        return max_fun_party(root.children[0])
    # Calcular la suma de la diversión de los empleados que están en la fiesta
    fun_with_root = root.fun
    for child in root.children:
        fun_with_root += max_fun_party(child)[0]
    # Calcular la suma de la diversión de los empleados que no están en la fiesta
    fun_without_root = 0
    for child in root.children:
        fun_without_root += max_fun_party(child)[1]
    # Devolver la máxima de ambas sumas
    return (max(fun_with_root, fun_without_root), fun_without_root)

# Ejercicio 26
def distribute_gifts(root):
    # Asigna un número a cada regalo
    VACATION, PANCAKES, DOG_POOP = 1, 2, 3
    
    # Función auxiliar recursiva para asignar regalos a los nodos
    def label_node(node, parent_gift):
        # Caso base: nodo hoja
        if not node.children:
            options = [VACATION, PANCAKES, DOG_POOP]
            options.remove(parent_gift)
            node.gift = options[0]
            return 0
        
        # Inicializar el mínimo costo como infinito
        min_cost = float('inf')
        
        # Probar cada opción de regalo
        for gift in [VACATION, PANCAKES, DOG_POOP]:
            # No asignar el mismo regalo que el padre
            if gift == parent_gift:
                continue
            
            # Asignar el regalo a este nodo
            node.gift = gift
            cost = sum(label_node(child, gift) for child in node.children)
            
            # Actualizar el mínimo costo
            min_cost = min(min_cost, cost)
        
        # Devolver el mínimo costo más el costo de asignar el regalo a este nodoq
        return min_cost + int(node.gift != parent_gift)
    
    # Llamar a la función auxiliar con el nodo raíz
    return label_node(root, VACATION)


# Ejercicio 27

# a
def least_awkward_subset(k, root):
    def helper(node, k):
        if node is None:
            return float("inf"), set()
        if not node.children:
            return 0, {node.id}
        if k == 0:
            return float("inf"), set()
        left_val, left_set = helper(node.left, k-1)
        right_val, right_set = helper(node.right, k-1)
        left_right_val, left_right_set = helper(node.left.right, k-2) if node.left and node.left.right else (float("inf"), set())
        right_left_val, right_left_set = helper(node.right.left, k-2) if node.right and node.right.left else (float("inf"), set())
        include_val = node.fun + left_right_val + right_left_val
        include_set = {node.id} | left_right_set | right_left_set
        exclude_val = left_val + right_val
        exclude_set = left_set | right_set
        if include_val < exclude_val:
            return include_val, include_set
        else:
            return exclude_val, exclude_set
    return helper(root, k)[0] if k > 0 else 0

#b
from math import inf

def least_awkward_subset2(k, root):
    def helper(node, k):
        if not node:
            return 0, set()
        if len(node.children) == 0:
            return node.fun, {node.id}
        if k <= 0:
            return inf, set()

        min_val = inf
        min_set = set()
        for i in range(len(node.children)):
            for j in range(i+1, len(node.children)):
                left_val, left_set = helper(node.children[i], k-2)
                right_val, right_set = helper(node.children[j], k-2)
                if left_val + right_val + node.fun < min_val:
                    min_val = left_val + right_val + node.fun
                    min_set = left_set.union(right_set).union({node.id})
        return min_val, min_set

    return helper(root, k)[1] if k > 0 else set()



# Prueba

	
root = Employee(1, 0)
root.children = [Employee(2, 2), Employee(3, 3)]
root.children[0].children = [Employee(4, -1), Employee(5, -1)]
root.children[1].children = [Employee(6, -2), Employee(7, -1)]

print(max_fun_party(root))

print(distribute_gifts(root))

print(least_awkward_subset(3, root))

print(least_awkward_subset2(7, root))