#include "arm/armTest.h"

using namespace arm;
using namespace ut;
using namespace test;
int main(int argc, char ** argv)
{
    string s(argv[0]);
    log_i("--- run : "+s);
    log_i("cur_dir:"+sys::pwd());
    bool ok = true;
    
    ArmTest t; ok &= t.run();
    if(ok) log_i("All test PASS!");
    else log_e("Failed");
    return ok?0:1;
}
