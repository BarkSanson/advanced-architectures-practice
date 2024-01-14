
#include <vector>
#include <oneapi/tbb/parallel_invoke.h>
#include <oneapi/tbb/parallel_for.h>
#include <oneapi/tbb/parallel_scan.h>

std::vector<int> gather_if(const std::vector<int>& vec, const std::vector<int>& conditions) {
    std::vector<int> indices(vec.size());
    int count = oneapi::tbb::parallel_scan(
        oneapi::tbb::blocked_range<int>(0, indices.size()),
        0,
        [&](const oneapi::tbb::blocked_range<int>& r, int last, bool is_final_scan) {
            int sum = last;
            for (int i = r.begin(); i < r.end(); i++) {
                if (conditions[i]) {
                    sum++;
                }
                if (is_final_scan) {
                    indices[i] = sum;
                }
            }
            return sum;
        },
        [](int left, int right) {
            return left + right;
        }
    );

    std::vector<int> gather(count);
    for (int i = 0; i < vec.size(); i++) {
        if (conditions[i]) {
            gather[indices[i] - 1] = vec[i];
        }
    }

    return gather;
}

std::vector<int> get_smaller_equal(const std::vector<int>& vec, int pivot) {
    std::vector<int> is_less_than_pivot(vec.size());
    for (auto i = 0; i < is_less_than_pivot.size(); i++) {
        is_less_than_pivot[i] = (vec[i] <= pivot);
    }

    return gather_if(vec, is_less_than_pivot);
}

std::vector<int> get_greater(const std::vector<int>& vec, int pivot) {
    std::vector<int> is_greater_than_pivot(vec.size());
    for (auto i = 0; i < vec.size(); i++) {
        is_greater_than_pivot[i] = (vec[i] > pivot);
    }

    return gather_if(vec, is_greater_than_pivot);
}


std::vector<int> quickSort(std::vector<int>& vec) {
    if (vec.size() <= 1) 
        return vec;
    
    int pivot = vec[vec.size() - 1]; 

    std::vector<int> left = get_smaller_equal(vec, pivot);
    std::vector<int> right = get_greater(vec, pivot);

    std::vector<int> left_result;
    std::vector<int> right_result;
    oneapi::tbb::task_group g;

    g.run([&] { left_result = quickSort(left); });
    g.run([&] { right_result = quickSort(right); });
    g.wait();

    std::vector<int> result(left_result.size() + right_result.size());
    std::copy(left_result.begin(), left_result.end(), result.begin());
    std::copy(right_result.begin(), right_result.end(), result.begin() + left_result.size());

    return result;
}