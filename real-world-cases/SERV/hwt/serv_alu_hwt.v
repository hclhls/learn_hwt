module serv_alu #(
    parameter B = 0,
    parameter W = 1
) (
    input wire clk,
    input wire[1:0] i_bool_op,
    input wire[0:0] i_buf,
    input wire i_cmp_eq,
    input wire i_cmp_sig,
    input wire i_cnt0,
    input wire i_en,
    input wire[0:0] i_op_b,
    input wire[2:0] i_rd_sel,
    input wire[0:0] i_rs1,
    input wire i_sub,
    output reg o_cmp,
    output reg[0:0] o_rd
);
    reg add_b;
    reg add_cy;
    reg add_cy_r;
    reg add_cy_r_next;
    reg cmp_r;
    reg cmp_r_next;
    reg op_b_sx;
    reg result_add;
    reg result_bool;
    reg result_eq;
    reg result_lt;
    reg result_slt;
    reg rs1_sx;
    always @(i_op_b, i_sub) begin: assig_process_add_b
        add_b = i_op_b[0] ^ i_sub;
    end

    always @(add_b, add_cy_r, i_rs1) begin: assig_process_add_cy
        reg[1:0] tmp_concat_0;
        reg[1:0] tmp_concat_1;
        reg[1:0] tmp_concat_2;
        reg[1:0] tmp_index_0;
        tmp_concat_0 = {1'b0, i_rs1};
        tmp_concat_1 = {1'b0, add_b};
        tmp_concat_2 = {1'b0, add_cy_r};
        tmp_index_0 = tmp_concat_0 + tmp_concat_1 + tmp_concat_2;
        add_cy = tmp_index_0[1];
    end

    always @(add_cy, cmp_r, i_en, i_sub, o_cmp) begin: assig_process_add_cy_r_next
        add_cy_r_next = 1'b0;
        if (i_en == 1'b1) begin
            add_cy_r_next = add_cy;
            cmp_r_next = o_cmp;
        end else begin
            add_cy_r_next = i_sub;
            cmp_r_next = cmp_r;
        end
    end

    always @(posedge clk) begin: assig_process_cmp_r
        cmp_r <= cmp_r_next;
        add_cy_r <= add_cy_r_next;
    end

    always @(i_cmp_eq, result_eq, result_lt) begin: assig_process_o_cmp
        o_cmp = i_cmp_eq ? result_eq : result_lt;
    end

    always @(i_buf, i_rd_sel, result_add, result_bool, result_slt) begin: assig_process_o_rd
        o_rd[0] = i_buf[0] | (i_rd_sel[0] & result_add) | (i_rd_sel[1] & result_slt) | (i_rd_sel[2] & result_bool);
    end

    always @(i_cmp_sig, i_op_b) begin: assig_process_op_b_sx
        op_b_sx = i_op_b[0] & i_cmp_sig;
    end

    always @(add_b, add_cy_r, i_rs1) begin: assig_process_result_add
        reg[1:0] tmp_concat_0;
        reg[1:0] tmp_concat_1;
        reg[1:0] tmp_concat_2;
        reg[1:0] tmp_index_0;
        tmp_concat_0 = {1'b0, i_rs1};
        tmp_concat_1 = {1'b0, add_b};
        tmp_concat_2 = {1'b0, add_cy_r};
        tmp_index_0 = tmp_concat_0 + tmp_concat_1 + tmp_concat_2;
        result_add = tmp_index_0[0];
    end

    always @(i_bool_op, i_op_b, i_rs1) begin: assig_process_result_bool
        reg[0:0] tmp_index_0;
        tmp_index_0 = i_rs1 ^ i_op_b;
        result_bool = tmp_index_0[0] & ~i_bool_op[0] | (i_bool_op[1] & i_op_b[0] & i_rs1[0]);
    end

    always @(cmp_r, i_cnt0, result_add) begin: assig_process_result_eq
        result_eq = result_add == 1'b0 & (cmp_r | i_cnt0) == 1'b1;
    end

    always @(add_cy, op_b_sx, rs1_sx) begin: assig_process_result_lt
        reg[0:0] tmp_index_0;
        tmp_index_0 = rs1_sx + ~op_b_sx + add_cy;
        result_lt = tmp_index_0[0];
    end

    always @(cmp_r, i_cnt0) begin: assig_process_result_slt
        result_slt = cmp_r & i_cnt0;
    end

    always @(i_cmp_sig, i_rs1) begin: assig_process_rs1_sx
        rs1_sx = i_rs1[0] & i_cmp_sig;
    end

    generate if (B != 0)
        $error("%m Generated only for this param value");
    endgenerate

    generate if (W != 1)
        $error("%m Generated only for this param value");
    endgenerate

endmodule

