#include <iostream>
#include <chrono>
#include <atomic>
#include <mutex>
#include <cmath>

#include "ReplayBuffer.hh"

#include "utility.hh"


std::mutex mtx;
int main(){
  constexpr auto buffer_size = 102400;
  constexpr auto N = 50000;
  constexpr auto M = 1000;

  auto idx = ymd::RingIndex<false>(buffer_size);
  auto stat = Stat();

  auto safe_idx = ymd::RingIndex<true>(buffer_size);
  auto safe_stat = Stat();

  auto lock_idx = ymd::RingIndex<false>(buffer_size);
  auto lock_stat = Stat();

  for(auto j = 0; j < M; ++j){
    stat.Add(measure([&,i=0]() mutable { idx.fetch_add(i++); },N));
    safe_stat.Add(measure([&,i=0]() mutable { safe_idx.fetch_add(i++); },N));
    lock_stat.Add(measure([&,i=0]() mutable {
			    std::lock_guard<std::mutex> lck(mtx);
			    lock_idx.fetch_add(i++);
			  },N));
  }


  std::cout << "RingIndex:           ";
  stat.stat();

  std::cout << "ThreadSafeRingIndex: ";
  safe_stat.stat();

  std::cout << "RingIndex with lock: ";
  lock_stat.stat();

  return 0;
}
