import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetailWorkspaceComponent } from './detail-workspace.component';

describe('DetailWorkspaceComponent', () => {
  let component: DetailWorkspaceComponent;
  let fixture: ComponentFixture<DetailWorkspaceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DetailWorkspaceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DetailWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
