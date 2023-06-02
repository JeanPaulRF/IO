# Ejercicio 5
# a
def palindromo_mas_largo(s):
    n = len(s)
    dp = [[0]*n for _ in range(n)] # matriz de n x n
    for i in range(n):
        dp[i][i] = 1
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i+l-1
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]

# b
def supersecuencia_palindromo_mas_corta(s):
    n = len(s)
    rev_s = s[::-1]
    dp = [[0] * (n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, n+1):
            if s[i-1] == rev_s[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return n + n - dp[n][n]

# c
def is_palindrome(s):
    return s == s[::-1]

def min_palindrome_decomposition(s):
    n = len(s)
    dp = [[float("inf") for _ in range(n+1)] for _ in range(n+1)]
    for i in range(n):
        dp[i][i] = 1
    
    for l in range(2, n+1):
        for i in range(n-l+1):
            j = i + l
            if is_palindrome(s[i:j]):
                dp[i][j] = 1
            else:
                for k in range(i+1, j):
                    dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])
    
    return dp[0][n]


# Pruebas

#print(palindromo_mas_largo("MAHDYNAMICPROGRAMZLETMESHOWYOUTHEM"))

#print(supersecuencia_palindromo_mas_corta("TWENTYONE"))

#print(min_palindrome_decomposition("BUBBASEESABANANA"))


# Ejercicio 25
def secuencia_digital_mas_larga(digits):
    n = len(digits)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if digits[i] > digits[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


# Prueba

# print(secuencia_digital_mas_larga([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4, 6, 2, 6, 4, 3, 3, 8, 3, 2, 7, 9]))