# 项目总结

## 项目背景

把LTL公式转换成等价自动机(通常是Buchi自动机)已经研究了近三十年。这种转换在基于自动机的模型检验中起着关键作用:首先构造否定LTL性质的自动机，然后将验证过程简化为自动机的空问题（emptiness problem）。格特等人提出了一种从LTL公式生成Buchi自动机的动态构造方法，这意味着即使只构造了部分属性自动机，也可以检测反例。他们称之为tableau构造方法，这种方法被广泛使用。

而在《On the Relationship between LTL Normal Forms andBuchi Automata》这篇论文中，作者们提出了一个新的结构，利用了析取范式的概念(DNF)。对于LTL公式，它的DNF范式是$\bigvee_i(\alpha_i \land X \varphi_i)$形式的等价公式，其中$\alpha_i$是有限字(原子命题或它们的否定)的合取，而$\varphi_i$是LTL公式的合取，因此它的根算符不是析取。

论文中证明了任何LTL公式可以转换成等价的DNF范式，并将$(\alpha_i \land X \varphi_i)$称为子句（`clause`)。很容易看出，任何给定的LTL公式都归纳了一个标记的迁移系统(LTS: labelled transition system)。

特别地，对于`Until/Release-Free`的LTL的公式，只需要分情况对LTS进行终止状态的标识即可构成Buchi自动机。

故本项目即为对其理论的具体实现。

## 约定

为了便于程序的输入输出，我们对于LTL的符号进行确认或改写。

1. Next : X
2. Release : R
3. Until : U
4. /\ : A
5. \/ : O
6. atomic proposition: a~z
7. parentheses : ), (
8. True: T
9. False: F

其中，论文中所考虑的是LTL公式的`NNF`形式，即所有的否定都会被压缩到`literal level`。因此，本项目不考虑否定符号。

另外，`G`，即`Always`也在论文提及可用`Release`等价替换，就不在此赘述。

## 思路分析

1. 拆分LTL公式
   
   ![Lemma](Images/Lemma.JPG)
