<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# how do i multiple a 3x2 matrix times a 2x4 

To multiply a **3x2 matrix** by a **2x4 matrix**, the result is a **3x4 matrix**.[^1_1][^1_2][^1_5]

## Matrix Multiplication Steps

- The number of columns in the first matrix (2) must equal the number of rows in the second (2).[^1_2][^1_1]
- For each entry in row $i$, column $j$ of the product:
    - Multiply elements of row $i$ of the first matrix by corresponding elements of column $j$ of the second matrix.
    - Sum those products. This is the dot product of a row from the first and a column from the second.[^1_7][^1_2]


## Example Calculation

Let \$ A \$ be the $3 \times 2$ matrix and \$ B \$ be the $2 \times 4$ matrix:

$$
A =
\begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22} \\
a_{31} & a_{32}
\end{pmatrix}
,\quad
B =
\begin{pmatrix}
b_{11} & b_{12} & b_{13} & b_{14} \\
b_{21} & b_{22} & b_{23} & b_{24}
\end{pmatrix}
$$

The product $AB$ entry at row $i$, column $j$ is:

$$
(AB)_{ij} = a_{i1} b_{1j} + a_{i2} b_{2j}
$$

Repeat for all combinations of row $i$ (from 1 to 3) and column $j$ (from 1 to 4).[^1_1][^1_2]

## Properties

- The product is not commutative: $(AB) \ne (BA)$.[^1_1]
- The resulting matrix has the shape **3x4**.[^1_2]


## Key Points

- Always match inner dimensions ( in 3x2 and 2x4).[^1_2][^1_1]
- Each entry in the result comes from a row-column dot product.[^1_7][^1_2]

This method works for any compatible matrices; just ensure inner dimensions match and build the result by row-column multiplication.
<span style="display:none">[^1_10][^1_3][^1_4][^1_6][^1_8][^1_9]</span>

<div style="text-align: center">⁂</div>

[^1_1]: https://www.cuemath.com/algebra/multiplication-of-matrices/

[^1_2]: https://www.mytutor.co.uk/answers/7783/A-Level/Maths/How-do-I-multiply-two-matrices-together/

[^1_3]: https://bathmash.github.io/HELM/7_2_matrix_multiplication-web/7_2_matrix_multiplication-webse6.html

[^1_4]: https://www.youtube.com/watch?v=2spTnAiQg4M

[^1_5]: https://en.wikipedia.org/wiki/Matrix_multiplication

[^1_6]: https://www.youtube.com/watch?v=8NraxDYRsFE

[^1_7]: https://www.mathsisfun.com/algebra/matrix-multiplying.html

[^1_8]: https://www.youtube.com/watch?v=7zdg7c9GaO4

[^1_9]: https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:properties-of-matrix-multiplication/a/properties-of-matrix-multiplication

[^1_10]: https://matrix.reshish.com/matrix-multiplication/


---

# shoe me an example

Here’s a concrete example of multiplying a **3x2 matrix** by a **2x4 matrix**. The result is a **3x4 matrix**.[^2_4][^2_6]

### Matrices

Let

$$
A = \begin{pmatrix}
2 & 3 \\
4 & 1 \\
-1 & 0
\end{pmatrix}
$$

and

$$
B = \begin{pmatrix}
5 & 2 & 4 & -3 \\
1 & 0 & 7 & 8
\end{pmatrix}
$$

### Multiplication

Each entry in the result is the dot product of a row from $A$ and a column from $B$:[^2_4]

$$
\text{Result} = A \times B = 
\begin{pmatrix}
2 \cdot 5 + 3 \cdot 1 & 2 \cdot 2 + 3 \cdot 0 & 2 \cdot 4 + 3 \cdot 7 & 2 \cdot {(-3)} + 3 \cdot 8 \\
4 \cdot 5 + 1 \cdot 1 & 4 \cdot 2 + 1 \cdot 0 & 4 \cdot 4 + 1 \cdot 7 & 4 \cdot {(-3)} + 1 \cdot 8 \\
-1 \cdot 5 + 0 \cdot 1 & -1 \cdot 2 + 0 \cdot 0 & -1 \cdot 4 + 0 \cdot 7 & -1 \cdot {(-3)} + 0 \cdot 8
\end{pmatrix}
$$

Calculating each entry:

- Row 1: \$ [2 \cdot 5 + 3 \cdot 1 = 10 + 3 = 13] \$, \$ [2 \cdot 2 + 3 \cdot 0 = 4 + 0 = 4] \$, \$ [2 \cdot 4 + 3 \cdot 7 = 8 + 21 = 29] \$, \$ [2 \cdot (-3) + 3 \cdot 8 = -6 + 24 = 18] \$
- Row 2: \$ [4 \cdot 5 + 1 \cdot 1 = 20 + 1 = 21] \$, \$ [4 \cdot 2 + 1 \cdot 0 = 8 + 0 = 8] \$, \$ [4 \cdot 4 + 1 \cdot 7 = 16 + 7 = 23] \$, \$ [4 \cdot (-3) + 1 \cdot 8 = -12 + 8 = -4] \$
- Row 3: \$ [-1 \cdot 5 + 0 \cdot 1 = -5 + 0 = -5] \$, \$ [-1 \cdot 2 + 0 \cdot 0 = -2 + 0 = -2] \$, \$ [-1 \cdot 4 + 0 \cdot 7 = -4 + 0 = -4] \$, \$ [-1 \cdot (-3) + 0 \cdot 8 = 3 + 0 = 3] \$


### Final Product

$$
A \times B = \begin{pmatrix}
\textbf{13} & \textbf{4} & \textbf{29} & \textbf{18} \\
\textbf{21} & \textbf{8} & \textbf{23} & \textbf{-4} \\
\textbf{-5} & \textbf{-2} & \textbf{-4} & \textbf{3}
\end{pmatrix}
$$

[^2_6][^2_4]

This demonstrates multiplying a 3x2 by a 2x4 matrix step by step.
<span style="display:none">[^2_1][^2_2][^2_3][^2_5][^2_7][^2_8][^2_9]</span>

<div style="text-align: center">⁂</div>

[^2_1]: https://people.richland.edu/james/lecture/m116/matrices/multiplication.html

[^2_2]: https://www.youtube.com/watch?v=2spTnAiQg4M

[^2_3]: https://www.youtube.com/watch?v=N3WT8_TWDYs

[^2_4]: https://www.mytutor.co.uk/answers/7783/A-Level/Maths/How-do-I-multiply-two-matrices-together/

[^2_5]: http://onlineprecaltextbook.weebly.com/matricies.html

[^2_6]: https://www.youtube.com/watch?v=8NraxDYRsFE

[^2_7]: https://matrix.reshish.com/matrix-multiplication/

[^2_8]: https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/v/multiplying-a-matrix-by-a-matrix

[^2_9]: https://www.khanacademy.org/math/precalculus/x9e81a4f98389efdf:matrices/x9e81a4f98389efdf:multiplying-matrices-by-matrices/a/multiplying-matrices


---

# save this in pdf?

The PDF creation could not be completed due to a missing module in the environment. However, the matrix multiplication example is ready for export and can be copied directly into any PDF tool or online PDF editor.[^3_1][^3_2]

## Matrix Multiplication Example Text

To save, simply copy the following text into a PDF generator (Word, Google Docs, Acrobat, or any online PDF conversion site):

***
**Example: Multiplying a 3x2 Matrix by a 2x4 Matrix**

Let
$A = \begin{pmatrix}2 & 3 \\ 4 & 1 \\ -1 & 0\end{pmatrix}$
$B = \begin{pmatrix}5 & 2 & 4 & -3 \\ 1 & 0 & 7 & 8\end{pmatrix}$

Step-by-step Product ($C = A \times B$):

- Row 1: [2*5 + 3*1 = 13], [2*2 + 3*0 = 4], [2*4 + 3*7 = 29], [2*(-3) + 3*8 = 18]
- Row 2: [4*5 + 1*1 = 21], [4*2 + 1*0 = 8], [4*4 + 1*7 = 23], [4*(-3) + 1*8 = -4]
- Row 3: [-1*5 + 0*1 = -5], [-1*2 + 0*0 = -2], [-1*4 + 0*7 = -4], [-1*(-3) + 0*8 = 3]

Final Product:

$$
\begin{pmatrix}
13 & 4 & 29 & 18 \\
21 & 8 & 23 & -4 \\
-5 & -2 & -4 & 3
\end{pmatrix}
$$
***

For a true PDF file, use this template in Word or Google Docs and export as PDF.[^3_2][^3_1]

<div style="text-align: center">⁂</div>

[^3_1]: https://www.mytutor.co.uk/answers/7783/A-Level/Maths/How-do-I-multiply-two-matrices-together/

[^3_2]: https://www.youtube.com/watch?v=8NraxDYRsFE

