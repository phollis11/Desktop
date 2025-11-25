#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {10, 20, 30};
    try {
        cout << v.at(3); // at() checks bounds
    } catch (out_of_range &e) {
        cout << "Error: " << e.what();
    }
    return 0;
}