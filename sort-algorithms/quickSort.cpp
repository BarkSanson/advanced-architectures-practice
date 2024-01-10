#include "quickSort.hpp"

int partition(std::vector<int>& vec, std::size_t low, std::size_t high) {
    int pivot = vec[high];

    std::size_t i = low - 1;

    for (std::size_t j = low; j < high; j++) {
        if (vec[j] < pivot) {
            i++;
            std::swap(vec[i], vec[j]);
        }
    }

    std::swap(vec[i + 1], vec[high]);

    return i + 1;
}

void quickSort(std::vector<int>& vec, std::size_t low, std::size_t high) {
    if (low < high) {
        int pivot = partition(vec, low, high);

        quickSort(vec, low, pivot - 1);
        quickSort(vec, pivot + 1, high);
    }
}