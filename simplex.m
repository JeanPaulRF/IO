function simplex()
  disp("\n---------------------------- Simplex ----------------------------\n");
  disp("Creadores:");
  disp("Jean Paul Rodriguez Flores");
  disp("Esteban\n");
  matriz = input("Digite la matriz de datos: ");

  identificador = matriz(1, end-1);

  if identificador == 1
    crear_max(matriz);
  else
    if identificador == -1
      crear_min(matriz);
    end
  end
end

function crear_max(matriz)
  c = matriz(1, 1:end-2);
  A = matriz(2:end, 1:end-2);
  cB = zeros(1, size(A,1));
  b = matriz(2:end, end);
  B1 = eye(size(A,1));
  xB = cB;

  for i = 1:size(xB, 2)
    xB(i) = i + size(A, 2);
  endfor

  C = horzcat(c, cB);

  [B1, xB] = simplex_revisado(c*-1, cB, A, B1, b, xB);

  cB = C(xB);

  newMat = [cB*B1*A-c, cB*B1, cB*B1*b; B1*A, B1, B1*b];

  disp("\nValor optimo: \t");
  disp(cB*B1*b);
  disp("\nVariables basicas: ");
  disp(xB);
  disp("\nPrecios sombra de las ecuaciones");
  disp(cB*B1);
  disp("\nMatriz completa del problema final: \n")
  imprimir_matriz(newMat);
end

function crear_min(matriz)
  %crear newMat para el caso de minimizacion

  %simplex_revisado(matriz);
end

function [B1, xB] = simplex_revisado(c, cB, A, B1, b, xB)
  minimo = min(c); %obtiene el valor minimo
  while minimo < 0

    columna = find(c == minimo, 1); %la columna del valor minimo

    filas_positivas = find(A(:, columna) > 0); % Encuentra las filas donde el valor es mayor a 0
    [~, min_fila] = min(b(filas_positivas) ./ A(filas_positivas, columna)); % Encuentra la fila con el valor mínimo
    fila = filas_positivas(min_fila); % Obtiene el índice de la fila original

    [A, B1, b, xB] = make_uno(A, B1, b, xB, columna, fila);

    [c, cB, A, B1, b] = make_ceros(c, cB, A, B1, b, columna, fila);


    minimo = min(c);
  endwhile
end

function [A, B1, b, xB] = make_uno(A, B1, b, xB, columna, fila)
  if A(fila, columna) ~= 1
    multiplicador = 1 / A(fila, columna);

    for i = 1:size(A, 2) %de 1 al numero de columnas de A
      A(fila, i) *= multiplicador;
    endfor

    for i = 1:size(B1, 2) %de 1 al numero de columnas de B1
      if B1(fila, i) == 1 %cambio de variable basica en xB
        xB(i) = columna;
      endif
      B1(fila, i) *= multiplicador;
    endfor

    b(fila) *= multiplicador;
  end
end

function [c, cB, A, B1, b] = make_ceros(c, cB, A, B1, b, columna, fila)
  for j = size(A, 1):-1:1 %del numero de filas de A, B1 y b a 1
    if j == fila || A(j, columna) == 0
      continue;
    endif

    if columna <= size(A, 2)
      sumador = A(j, columna) * -1;
    else
      sumador = B1(j, columna) * -1;
    end

    %disp(sumador);

    for i = 1:size(A, 2) %de 1 al numero de columnas de A
      A(j, i) += sumador * A(fila, i);
    endfor

    for i = 1:size(B1, 2) %de 1 al numero de columnas de B1
      B1(j, i) += sumador * B1(fila, i);
    endfor

    b(j) += sumador *b(fila);
  endfor

  if columna <= size(c, 2)
    sumador = c(columna) * -1;
  else
    sumador = cB(columna) * -1;
  end

  for i = 1:size(c, 2) %de 1 al numero de columnas de c
    c(i) += sumador * A(fila, i);
  endfor

  for i = 1:size(cB, 2) %de 1 al numero de columnas de cB
    cB(i) += sumador * B1(fila, i);
  endfor
end


function imprimir_matriz(A)
  formato = "\t%.4f";
  str = "";
  for i = 1:size(A, 1)
    for j = 1:size(A, 2)
      str = strcat(str, sprintf(formato, A(i,j)), "");
    endfor
    str = strcat(str, "\n");
  endfor
  disp(str);
end
