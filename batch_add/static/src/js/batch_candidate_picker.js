/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class BatchCandidatePicker extends Component {
  static template = "batch_add.BatchCandidatePicker";
  static props = {
    ...standardFieldProps,
  };

  get candidateRecords() {
    const recordList = this.props.record.data[this.props.name];
    return recordList?.records || [];
  }

  async selectCandidate(candidate) {
    const resId = candidate?.resId;
    if (!resId) return;
    const displayName = candidate?.data?.display_name || "";
    await this.props.record.update({ product_id: [resId, displayName] });
  }
}

export const batchCandidatePicker = {
  component: BatchCandidatePicker,
  supportedTypes: ["many2many"],
  relatedFields: () => [{ name: "display_name", type: "char" }],
};

registry.category("fields").add("batch_candidate_picker", batchCandidatePicker);
