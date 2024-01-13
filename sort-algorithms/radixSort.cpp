#include <iostream>
#include <vector>
#include <bitset>
#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/parallel_scan.h>
#include <oneapi/tbb/blocked_range.h>

#include "radixSort.hpp"

std::vector<int> radixSort(std::vector<int>& vec, int size) {
    int bits = 10;

    std::vector<int> out(vec);
    for (int i = 0; i < bits; i++) {
        std::vector<bool> bits(size);

        // Map numbers to the bit at the current index
        for (int j = 0; j < size; j++) {
            bits[j] = (out[j] >> i) & 1;
        }

        // Scan the bits to find the index of the 0s
        std::vector<int> index_zero(size);
        int last_index_zero = oneapi::tbb::parallel_scan(
            oneapi::tbb::blocked_range<int>(0, size),
            0,
            [&](const oneapi::tbb::blocked_range<int> r, int last, bool is_final_scan) {
                int sum = last;
                for (int j = r.begin(); j < r.end(); j++) {
                    if (!bits[j]) {
                        sum++;
                    }
                    if (is_final_scan) {
                        index_zero[j] = sum;
                    }
                }
                return sum;
            },
            [](int left, int right) {
                return left + right;
            }
        );

        // Now, same but for 1s. Note that it's necessary
        // to add last_index_zero to the sum
        std::vector<int> index_one(size);
        int last_index_one = oneapi::tbb::parallel_scan(
            // Do the same as above, but starting from last_index_zero
            oneapi::tbb::blocked_range<int>(0, size),
            0,
            [&](const oneapi::tbb::blocked_range<int> r, int last, bool is_final_scan) {
                int sum = last;
                for (int j = r.begin(); j < r.end(); j++) {
                    if (bits[j]) {
                        sum++;
                    }
                    if (is_final_scan) {
                        index_one[j] = sum + last_index_zero;
                    }
                }
                return sum;
            },
            [](int left, int right) {
                return left + right;
            }
        );

        // Finally, just reorder the array based
        // on the indices
        std::vector<int> temp(size);
        for (int j = 0; j < size; j++) {
            if (bits[j]) {
                temp[index_one[j] - 1] = out[j];
            } else {
                temp[index_zero[j] - 1] = out[j];
            }
        }

        out = temp;
    }

    return out; 
}

