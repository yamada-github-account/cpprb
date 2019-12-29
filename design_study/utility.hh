#ifndef CPPRB_UTILITY_HH
#define CPPRB_UTILITY_HH

#include <iostream>
#include <chrono>
#include <cmath>
#include <utility>

class Stat {
  unsigned long long N;
  long double x;
  long double xx;

public:
  Stat(): N{0},x{0},xx{0} {}
  void Add(double _x){
    ++N;
    x += _x;
    xx += _x*_x;
  }
  double Average() const {
    return (double) x/N;
  }
  double Std() const {
    auto ave = Average();
    return (double)std::sqrt(xx/N - ave*ave);
  }
  void stat() const {
    std::cout << Average()
	      << " +/- "
	      << Std()
	      << " ns"
	      << std::endl;
  }
};

template<typename F,typename...Args> auto measure(F&& f,std::size_t N,Args&&...args){
  auto start = std::chrono::high_resolution_clock::now();
  for(std::size_t i = 0; i < N; ++i){
    f(std::forward<Args>(args)...);
  }
  auto end = std::chrono::high_resolution_clock::now();

  return std::duration_cast<std::chrono::nanoseconds>(end - start).count();
}


#endif // CPPRB_UTILITY
