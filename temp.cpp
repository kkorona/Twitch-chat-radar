#include <iostream>
#include <functional>
#include <string>
#include <vector>
#include <array>
 
class EvenOddFunctor
{
public:
     EvenOddFunctor() : evenSum(0), oddSum(0) {}
 
     void operator() (int x)
     {
          if(x%2 == 0)
              evenSum += x;
          else
              oddSum += x;
     }
     int sumEven() const {return evenSum;}
     int sumOdd() const {return oddSum;}
 
private:
     int evenSum;
     int oddSum;
};
 
int main(void)
{
    EvenOddFunctor functor;
    std::array<int, 10> theList = {1,2,3,4,5,6,7,8,9,10}; // Uniform Initialization 으로 초기화
    functor = std::for_each(theList.cbegin(), theList.cend(), functor); // cBegin(처음) 부터 cEnd(마지막) 까지 체크해서 functor(opeartor()(int x)) 에 넘김 그러면 각각의 숫자를 넣은 operator 함수의 값을 체크해서 functor (EvenOddFunctor)을 넘겨줌. 그러면 현재 EvenOddFunctor인 functor에 넣어줌으로써 evenSum, oddSum등의 변수를 저장하게 된다.
     
    std::cout << "Sum of evens: " << functor.sumEven() << std::endl;
    std::cout << "Sum of odds: " << functor.sumOdd() << std::endl;
 
    getchar();
    return 0;
}
