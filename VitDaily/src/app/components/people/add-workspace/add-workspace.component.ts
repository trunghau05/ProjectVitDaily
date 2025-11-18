import { CommonModule } from '@angular/common';
import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { WorkSpace, Member } from '../../../models/people/workspace.interface';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-add-workspace',
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './add-workspace.component.html',
  styleUrl: './add-workspace.component.scss'
})
export class AddWorkspaceComponent {
  @Output() close = new EventEmitter<void>();
  @Output() add = new EventEmitter<void>();

  newWorkspace = {} as WorkSpace;
  members: Member[]  = [];
  newMembers = [];
  email = '';
  role = '';

  constructor(private workspaceService: WorkspaceService, private userService: UserService) {}

  closeAdd() {
    this.close.emit();
  }

  async addWorkspace() {
    try {
      this.newWorkspace.members = this.members;
      const response = await this.workspaceService.addWorkspace(this.newWorkspace);
      console.log(response);
      alert("Thêm workspace thành công!");
      this.add.emit();
    } catch (error) {
      console.error("Lỗi khi thêm workspace:", error);
    }
  }

  async addUserByEmail() {
    try {
      const response = await this.userService.getUserByEmail(this.email);
      const user = response;      
      const today = new Date();

      if (user) {
        const member: Member = {
          us_id: user.us_id,
          us_name: user.us_name,
          us_img: user.us_img,
          role: this.role || 'member',
          joined_at: today.toISOString()
        };
        this.members.push(member);
        this.email = '';
        this.role = '';
      }
    } catch (error) {
      console.error("Lỗi khi lấy user theo email:", error);
    }
  }

  removeMember(index: number) {
    this.members.splice(index, 1);
  }
}
