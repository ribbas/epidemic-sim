#include <math.h>

#include <systemc.h>

SC_MODULE(sc_floor) {
    sc_in<float> operand;
    sc_out<sc_uint<25> > data_out;

    void do_floor() {
        data_out.write(floor(operand.read()));
    }

    SC_CTOR(sc_floor) {
        SC_METHOD(do_floor);
        sensitive << operand;
    }
};
