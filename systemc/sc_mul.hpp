#include <math.h>

#include <systemc.h>

SC_MODULE(sc_mul) {
    sc_in<float> operandf;
    sc_out<float> data_out;

    void do_mul() {
        data_out.write(2 * (operandf.read()));
    }

    SC_CTOR(sc_mul) {
        SC_METHOD(do_mul);
        sensitive << operandf;
    }
};
