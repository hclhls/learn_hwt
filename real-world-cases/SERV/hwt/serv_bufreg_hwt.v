module serv_bufreg #(
    parameter B = 0,
    parameter MDU = 0,
    parameter W = 1
) (
    input wire i_clk,
    input wire i_clr_lsb,
    input wire i_cnt0,
    input wire i_cnt1,
    input wire i_en,
    input wire[0:0] i_imm,
    input wire i_imm_en,
    input wire i_init,
    input wire i_mdu_op,
    input wire[0:0] i_rs1,
    input wire i_rs1_en,
    input wire i_sh_signed,
    output reg[31:0] o_dbus_adr,
    output wire[31:0] o_ext_rs1,
    output reg[1:0] o_lsb,
    output reg[0:0] o_q
);
    reg c;
    reg c_r;
    reg c_r_next;
    reg clr_lsb;
    reg[31:0] data;
    reg[31:0] data_next;
    reg[1:0] data_next_1downto0;
    reg[29:0] data_next_31downto2;
    reg[1:0] lsb;
    wire mdu_on;
    reg q;
    always @(c_r, clr_lsb, i_imm, i_imm_en, i_rs1, i_rs1_en) begin: assig_process_c
        reg[1:0] tmp_concat_0;
        reg[1:0] tmp_concat_1;
        reg[1:0] tmp_concat_2;
        reg[1:0] tmp_index_0;
        tmp_concat_0 = {1'b0, i_rs1[0] & i_rs1_en};
        tmp_concat_1 = {1'b0, i_imm[0] & i_imm_en & ~clr_lsb};
        tmp_concat_2 = {1'b0, c_r};
        tmp_index_0 = tmp_concat_0 + tmp_concat_1 + tmp_concat_2;
        c = tmp_index_0[1];
    end

    always @(c, i_en) begin: assig_process_c_r_next
        c_r_next = c & i_en;
    end

    always @(i_clr_lsb, i_cnt0) begin: assig_process_clr_lsb
        clr_lsb = i_cnt0 & i_clr_lsb;
    end

    always @(posedge i_clk) begin: assig_process_data
        data <= data_next;
        c_r <= c_r_next;
    end

    always @(data_next_1downto0, data_next_31downto2) begin: assig_process_data_next
        data_next = {data_next_31downto2, data_next_1downto0};
    end

    always @(data, i_cnt0, i_cnt1, i_en, i_init, q) begin: assig_process_data_next_1downto0
        if (i_init ? i_cnt0 | i_cnt1 : i_en)
            data_next_1downto0 = {i_init ? q : data[2], data[1]};
        else
            data_next_1downto0 = data[1:0];
    end

    always @(data, i_en, i_init, i_sh_signed, q) begin: assig_process_data_next_31downto2
        if (i_en)
            data_next_31downto2 = {i_init ? q : data[31] & i_sh_signed, data[31:3]};
        else
            data_next_31downto2 = data[31:2];
    end

    always @(data) begin: assig_process_lsb
        lsb = data[1:0];
    end

    assign mdu_on = 1'b0;
    always @(data) begin: assig_process_o_dbus_adr
        o_dbus_adr = {data[31:2], 2'b00};
    end

    assign o_ext_rs1 = data;
    always @(i_mdu_op, lsb, mdu_on) begin: assig_process_o_lsb
        if (i_mdu_op & mdu_on)
            o_lsb = 2'b00;
        else
            o_lsb = lsb;
    end

    always @(data, i_en) begin: assig_process_o_q
        o_q[0] = data[0] & i_en;
    end

    always @(c_r, clr_lsb, i_imm, i_imm_en, i_rs1, i_rs1_en) begin: assig_process_q
        reg[1:0] tmp_concat_0;
        reg[1:0] tmp_concat_1;
        reg[1:0] tmp_concat_2;
        reg[1:0] tmp_index_0;
        tmp_concat_0 = {1'b0, i_rs1[0] & i_rs1_en};
        tmp_concat_1 = {1'b0, i_imm[0] & i_imm_en & ~clr_lsb};
        tmp_concat_2 = {1'b0, c_r};
        tmp_index_0 = tmp_concat_0 + tmp_concat_1 + tmp_concat_2;
        q = tmp_index_0[0];
    end

    generate if (B != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (MDU != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (W != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

