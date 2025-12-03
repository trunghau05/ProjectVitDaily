import { Routes } from '@angular/router';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { NoteComponent } from './pages/person/note/note.component';
import { AddNoteComponent } from './components/person/add-note/add-note.component';
import { DetailNoteComponent } from './components/person/detail-note/detail-note.component';
import { TaskComponent } from './pages/person/task/task.component';
import { VitaiComponent } from './components/vitai/vitai.component';
import { WorkspaceComponent } from './pages/people/workspace/workspace.component';
import { TeamComponent } from './pages/people/team/team.component';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'vitai', component: VitaiComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // Person
  { path: 'note', component: NoteComponent },
  { path: 'add-note', component: AddNoteComponent },
  { path: 'person/task', component: TaskComponent },
  { path: 'person/detail-note/:nt_id', component: DetailNoteComponent },
  
  // People
  { path: 'workspace', component: WorkspaceComponent },
  { path: 'workspace/:ws_id', component: TeamComponent},

];
