import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { WorkSpace, Member } from '../../../models/people/workspace.interface';
import { UserService } from '../../../services/user.service';
import { MemberService } from '../../../services/people/member.service';

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
  usId: string | null = sessionStorage.getItem('us_id');
  email = '';
  role = '';
  wsId = '';

  constructor(private workspaceService: WorkspaceService, private userService: UserService, private memberService: MemberService) {}

  closeAdd() {
    this.close.emit();
  }

  async addWorkspace() {
    try {
      this.newWorkspace.owner_id = this.usId || '';
      const response = await this.workspaceService.addWorkspace(this.newWorkspace);
      this.wsId = response.data.ws_id;
      console.log(response);
      console.log(this.wsId);
      alert("Thêm workspace thành công!");
    } catch (error) {
      console.error("Lỗi khi thêm workspace:", error);
    }

    try {
      const data: any = {ws_id: this.wsId, members: this.members};
      const response = await this.memberService.addMembers(data);
      console.log(response);
    } catch (error) {
      console.error("Lỗi khi thêm thành viên:", error);
    }

    this.add.emit();
    this.closeAdd();
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
