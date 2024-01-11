#include <iostream>
#include "quickSort.hpp"

int partition(std::vector<int>& vec, std::size_t low, std::size_t high) {
    std::cout << "Partitioning from " << low << " to " << high << std::endl;
    int pivot = vec[high];

    std::size_t i = low - 1;

    for (std::size_t j = low; j <= high; j++) {
        std::cout << "Comparing " << vec[j] << " and " << pivot << std::endl;
        if (vec[j] < pivot) {
            i++;
            std::cout << "Swapping " << vec[i] << " and " << vec[j] << std::endl;
            std::swap(vec[i], vec[j]);
        }

        std::cout << "i: " << i << std::endl;
        std::cout << "j: " << j << std::endl;
    }

    std::swap(vec[i + 1], vec[high]);

    std::cout << "Pivot index: " << i + 1 << std::endl;
    return i + 1;

}

void quickSort(std::vector<int>& vec, std::size_t low, std::size_t high) {
    if (low < high) {
        int pivot = partition(vec, low, high);

        quickSort(vec, low, pivot - 1);
        quickSort(vec, pivot + 1, high);
    }
}