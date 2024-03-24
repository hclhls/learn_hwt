module serv_aligner (
    input wire clk,
    input wire[31:0] i_ibus_adr,
    input wire i_ibus_cyc,
    input wire i_wb_ibus_ack,
    input wire[31:0] i_wb_ibus_rdt,
    output reg o_ibus_ack,
    output reg[31:0] o_ibus_rdt,
    output reg[31:0] o_wb_ibus_adr,
    output wire o_wb_ibus_cyc,
    input wire rst
);
    reg ack_en;
    reg ctrl_misal = 1'b0;
    reg ctrl_misal_next;
    reg[31:0] ibus_rdt_concat;
    reg[15:0] lower_hw;
    reg[15:0] lower_hw_next;
    always @(ctrl_misal, i_ibus_adr) begin: assig_process_ack_en
        ack_en = ~(i_ibus_adr[1] & ~ctrl_misal);
    end

    always @(posedge clk) begin: assig_process_ctrl_misal
        if (rst == 1'b1)
            ctrl_misal <= 1'b0;
        else
            ctrl_misal <= ctrl_misal_next;
    end

    always @(ctrl_misal, i_ibus_adr, i_wb_ibus_ack) begin: assig_process_ctrl_misal_next
        if (i_wb_ibus_ack & i_ibus_adr[1])
            ctrl_misal_next = ~ctrl_misal;
        else
            ctrl_misal_next = ctrl_misal;
    end

    always @(i_wb_ibus_rdt, lower_hw) begin: assig_process_ibus_rdt_concat
        ibus_rdt_concat = {i_wb_ibus_rdt[15:0], lower_hw};
    end

    always @(posedge clk) begin: assig_process_lower_hw
        lower_hw <= lower_hw_next;
    end

    always @(i_wb_ibus_ack, i_wb_ibus_rdt, lower_hw) begin: assig_process_lower_hw_next
        if (i_wb_ibus_ack)
            lower_hw_next = i_wb_ibus_rdt[31:16];
        else
            lower_hw_next = lower_hw;
    end

    always @(ack_en, i_wb_ibus_ack) begin: assig_process_o_ibus_ack
        o_ibus_ack = i_wb_ibus_ack & ack_en;
    end

    always @(ctrl_misal, i_wb_ibus_rdt, ibus_rdt_concat) begin: assig_process_o_ibus_rdt
        o_ibus_rdt = ctrl_misal ? ibus_rdt_concat : i_wb_ibus_rdt;
    end

    always @(ctrl_misal, i_ibus_adr) begin: assig_process_o_wb_ibus_adr
        o_wb_ibus_adr = ctrl_misal ? i_ibus_adr + 32'h00000004 : i_ibus_adr;
    end

    assign o_wb_ibus_cyc = i_ibus_cyc;
endmodule

