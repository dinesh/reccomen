
#include <iostream>
#include <fstream>
#include <marsyas/realvec.h>
#include <marsyas/NumericLib.h>

using namespace std;
using namespace Marsyas;


int main(int argc, char** argv)
{
        if (argc < 3) {
                cout << "Usage: " << argv[0] << "vec1 vec2" << endl;
                cout << "calculates the distance between two song feature vectors" << endl;
                return 1;
        }
        realvec v1;
        realvec v2;
        
        // empty vector for euclidean distance
        realvec cov;
        mrs_real res;
        
        // read in the vectors
        try {
                v1.read(argv[1]);
                v2.read(argv[2]);
        } catch (int i)
        {
                cout << "Error reading vectors" << endl;
                return 1;
        }
        
        // calculate the result
        try {
                res = NumericLib::euclideanDistance(v1, v2, cov);
        } catch (int i)
        {
                cout << "Error computing distance" << endl;
                return 1;
        }

        cout.setf(ios_base::fixed, ios_base::floatfield);
    cout.precision(12);
        
        cout << right << res << endl;
        return 0;
}

