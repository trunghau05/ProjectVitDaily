import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';
import { MatIconModule } from '@angular/material/icon';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { WorkSpace, Member } from '../../../models/people/workspace.interface';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { UserService } from '../../../services/user.service';
import { AddWorkspaceComponent } from '../../../components/people/add-workspace/add-workspace.component';
import { DetailWorkspaceComponent } from '../../../components/people/detail-workspace/detail-workspace.component';

@Component({
  selector: 'app-workspace',
  imports: [NavbarComponent, CommonModule, FormsModule, SearchBarComponent, MatIconModule, FlexCenterDirective, FormatDatePipe, AddWorkspaceComponent, DetailWorkspaceComponent],
  templateUrl: './workspace.component.html',
  styleUrl: './workspace.component.scss'
})
export class WorkspaceComponent implements OnInit {
  usId: string | null = sessionStorage.getItem('us_id');
  isAdd: boolean = false;
  isDetail: boolean = false;

  ownerWorkspaces: WorkSpace[] = [];
  memberWorkspaces: WorkSpace[] = [];
  workspaces: WorkSpace[] = [];

  imgs:  any[] = [];
  members: Member[] = [];
  wsId = '';

  constructor(private workspaceService: WorkspaceService, private userService: UserService) {}

  ngOnInit() {
    this.loadWorkspace(); 
  }

  async loadWorkspace() {
    if (!this.usId) {
      console.warn("User ID rỗng!");
      return;
    }

    try {
      const response = await this.workspaceService.getWorkspaceOwner(this.usId);
      this.ownerWorkspaces = response.data;
    } catch (error) {
      console.error("Lỗi khi lấy workspace owner:", error);
    }

    try {
      const response = await this.workspaceService.getWorkspaceMember(this.usId);
      this.memberWorkspaces = response.data;
    } catch (error) {
      console.error("Lỗi khi lấy workspace member:", error);
    }

    this.workspaces = [...this.ownerWorkspaces, ...this.memberWorkspaces];
    console.log(this.workspaces);
    
    this.members = this.workspaces.flatMap((m) => m.members ?? []);
  }

  getMemberImagesByWorkspace(workspace: WorkSpace): string[] {
    if (!workspace.members) return [];
    
    return workspace.members
      .slice(0, 3)
      .map(m => m.us_img || '/assets/default-avatar.png')
      .filter(img => img !== undefined);
  }

  openAdd() {
    this.isAdd = true;
  }

  closeAdd() {
    this.isAdd = false;
  }
  
  add() {
    this.ngOnInit();
  }

  closeDetail() {
    this.isDetail = false;
  }

  openDetail(ws_id: string) {
    this.wsId = ws_id;
    
    this.isDetail = true;
  }
}
