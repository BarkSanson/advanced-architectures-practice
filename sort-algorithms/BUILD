cc_library(
    name = "radixSort",
    srcs = ["radixSort.cpp"],
    hdrs = ["radixSort.hpp"],
    deps = [
        "@oneTBB//:tbb",
    ]
)

cc_library(
    name = "quickSort",
    srcs = ["quickSort.cpp"],
    hdrs = ["quickSort.hpp"],
    deps = [
        "@oneTBB//:tbb",
    ]
)

cc_library(
    name = "mergeSort",
    srcs = ["mergeSort.cpp"],
    hdrs = ["mergeSort.hpp"],
    deps = [
        "@oneTBB//:tbb",
    ]
)

cc_binary(
    name = "SortAlgorithms",
    srcs = ["main.cpp"],
    deps = [
        "@oneTBB//:tbb",
        ":mergeSort",
        ":quickSort",
        ":radixSort"
    ],
)
