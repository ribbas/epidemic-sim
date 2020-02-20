#include <systemc.h>

SC_MODULE(mul_inv) {
    sc_in<sc_uint<10> > operand;
    sc_out<float> data_out;

    void do_div() {
        data_out.write(1 / ((float) operand.read()));
    }

    SC_CTOR(mul_inv) {
        SC_METHOD(do_div);
        sensitive << operand;
    }
};
