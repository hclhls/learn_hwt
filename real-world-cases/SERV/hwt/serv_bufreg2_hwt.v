module serv_bufreg2 (
    input wire i_byte_valid,
    input wire i_clk,
    input wire i_cnt_done,
    input wire[31:0] i_dat,
    input wire i_en,
    input wire i_imm,
    input wire i_init,
    input wire i_load,
    input wire[1:0] i_lsb,
    input wire i_op_b_sel,
    input wire i_rs2,
    input wire i_shift_op,
    output wire[31:0] o_dat,
    output reg o_op_b,
    output reg o_q,
    output reg o_sh_done,
    output reg o_sh_done_r
);
    reg[31:0] dat;
    reg dat_en;
    reg[31:0] dat_next;
    reg[5:0] dat_shamt;
    always @(posedge i_clk) begin: assig_process_dat
        dat <= dat_next;
    end

    always @(i_byte_valid, i_en, i_shift_op) begin: assig_process_dat_en
        dat_en = i_shift_op | (i_en & i_byte_valid);
    end

    always @(dat, dat_en, dat_shamt, i_dat, i_load, o_op_b) begin: assig_process_dat_next
        reg[31:0] tmp_concat_0;
        tmp_concat_0 = {{o_op_b, dat[31:7]}, dat_shamt};
        if (dat_en | i_load)
            dat_next = i_load ? i_dat : tmp_concat_0;
        else
            dat_next = dat;
    end

    always @(dat, i_cnt_done, i_init, i_shift_op) begin: assig_process_dat_shamt
        if (i_shift_op & ~i_init)
            dat_shamt = dat[5:0] - 6'b000001;
        else
            dat_shamt = {dat[6] & ~(i_shift_op & i_cnt_done), dat[5:1]};
    end

    assign o_dat = dat;
    always @(i_imm, i_op_b_sel, i_rs2) begin: assig_process_o_op_b
        o_op_b = i_op_b_sel ? i_rs2 : i_imm;
    end

    always @(dat, i_lsb) begin: assig_process_o_q
        o_q = i_lsb == 2'b11 & dat[24] == 1'b1 | (i_lsb == 2'b10 & dat[16] == 1'b1) | (i_lsb == 2'b01 & dat[8] == 1'b1) | (i_lsb == 2'b00 & dat[0] == 1'b1);
    end

    always @(dat_shamt) begin: assig_process_o_sh_done
        o_sh_done = dat_shamt[5];
    end

    always @(dat) begin: assig_process_o_sh_done_r
        o_sh_done_r = dat[5];
    end

endmodule

