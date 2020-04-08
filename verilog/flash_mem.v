`timescale 1ns/1ps

module flash_mem #(
    parameter ADDR_WIDTH = 10,
    parameter DATA_WIDTH = 25
    ) (
    input wire [ADDR_WIDTH - 1:0] address,
    input wire [DATA_WIDTH - 1:0] data_in,
    output wire [DATA_WIDTH - 1:0] data_out,
    input wire cs, we, oe
);

    reg [DATA_WIDTH - 1:0] mem [0:(1 << ADDR_WIDTH) - 1];
    assign data_out = (cs && !we && oe) ? mem[address] : {DATA_WIDTH{1'bz}};

    always @(cs or we or oe or address) begin

        if (cs && we && !oe) begin
            mem[address] <= data_in;
        end

    end

endmodule
