import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { WorkSpace, Member } from '../../../models/people/workspace.interface';
import { UserService } from '../../../services/user.service';
import { MemberService } from '../../../services/people/member.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-detail-workspace',
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './detail-workspace.component.html',
  styleUrl: './detail-workspace.component.scss'
})
export class DetailWorkspaceComponent implements OnInit{
  @Input() wsId: string | null=null;
  @Output() close = new EventEmitter<void>();
  @Output() update = new EventEmitter<void>();

  workspace = {} as WorkSpace;
  members: Member[] = [];
  usId: string | null = sessionStorage.getItem('us_id');
  email = '';
  role = '';

  isOwner: boolean = false;

  ngOnInit(): void {
    this.loadWorkspaceDetail();
  }

  constructor(private workspaceService: WorkspaceService, private userService: UserService, private memberService: MemberService, private router: Router) {}

  closeDetail() {
    this.close.emit();
  }

  async loadWorkspaceDetail() {
    if (!this.wsId) {
      console.warn("Workspace ID rỗng!");
      return;
    }

    try {
      const response = await this.workspaceService.getWorkspaceDetail(this.wsId);
      this.workspace = response.data;
      this.members = this.workspace.members;

      if (this.usId === this.workspace.owner_id) {
        this.isOwner = true;
      }
      
    } catch (error) {
      console.error("Lỗi khi lấy chi tiết workspace:", error);
    }
  }

  async updateWorkspace() {
    try {
      const response = await this.workspaceService.updateWorkspace(this.workspace);
      console.log(response);
      alert("Cập nhật workspace thành công!");
    } catch (error) {
      console.error("Lỗi khi cập nhật workspace:", error);
    }

    this.update.emit();
    this.closeDetail();
  }

  async addUserByEmail() {
    try {
      const response = await this.userService.getUserByEmail(this.email);
      const user = response;
      const today = new Date().toISOString().split('T')[0]; 

      if (user) {
        const member: Member = {
          us_id: user.us_id,
          us_name: user.us_name,
          us_img: user.us_img,
          role: this.role || 'member',
          joined_at: today
        };
        this.members.push(member);  
        this.workspace.members = this.members;
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

  connectWorkspace(ws_id: string) {
    this.router.navigate(['workspace/', ws_id]);
  }
}
