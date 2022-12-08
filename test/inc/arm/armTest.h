#include "arm/armLib.h"

namespace test
{
    using namespace arm; 

    //-----
    class ArmTest : public Test{
    public:
        virtual bool run()override;
    protected:
        bool test_basic()const;
        bool test_moveTo()const;
    };


}

