module serv_mem_if #(
    parameter B = 0,
    parameter W = 1,
    parameter WITH_CSR = 1
) (
    input wire[0:0] i_bufreg2_q,
    input wire[1:0] i_bytecnt,
    input wire i_clk,
    input wire i_half,
    input wire[1:0] i_lsb,
    input wire i_mdu_op,
    input wire i_signed,
    input wire i_word,
    output reg o_byte_valid,
    output reg o_misalign,
    output reg[0:0] o_rd,
    output reg[3:0] o_wb_sel
);
    reg dat_valid;
    reg signbit;
    reg signbit_next;
    wire with_csr;
    always @(i_bytecnt, i_half, i_mdu_op, i_word) begin: assig_process_dat_valid
        dat_valid = (i_mdu_op | i_word) == 1'b1 | i_bytecnt == 2'b00 | (i_half & ~i_bytecnt[1]) == 1'b1;
    end

    always @(i_bytecnt, i_lsb) begin: assig_process_o_byte_valid
        o_byte_valid = ~i_lsb[0] & ~i_lsb[1] | (~i_bytecnt[0] & ~i_bytecnt[1]) | (~i_bytecnt[1] & ~i_lsb[1]) | (~i_bytecnt[1] & ~i_lsb[0]) | (~i_bytecnt[0] & ~i_lsb[1]);
    end

    always @(i_half, i_lsb, i_word, with_csr) begin: assig_process_o_misalign
        o_misalign = with_csr & (i_lsb[0] & (i_word | i_half) | (i_lsb[1] & i_word));
    end

    always @(dat_valid, i_bufreg2_q, i_signed, signbit) begin: assig_process_o_rd
        o_rd = dat_valid ? i_bufreg2_q : i_signed & signbit;
    end

    always @(i_half, i_lsb, i_word) begin: assig_process_o_wb_sel
        o_wb_sel = {{{i_lsb == 2'b11 | i_word == 1'b1 | (i_half & i_lsb[1]) == 1'b1, i_lsb == 2'b10 | i_word == 1'b1}, i_lsb == 2'b01 | i_word == 1'b1 | (i_half & ~i_lsb[1]) == 1'b1}, i_lsb == 2'b00};
    end

    always @(posedge i_clk) begin: assig_process_signbit
        signbit <= signbit_next;
    end

    always @(dat_valid, i_bufreg2_q, signbit) begin: assig_process_signbit_next
        if (dat_valid)
            signbit_next = i_bufreg2_q[0];
        else
            signbit_next = signbit;
    end

    assign with_csr = 1'b1;
    generate if (B != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (W != 1)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (WITH_CSR != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

