import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VitaiComponent } from './vitai.component';

describe('VitaiComponent', () => {
  let component: VitaiComponent;
  let fixture: ComponentFixture<VitaiComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VitaiComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VitaiComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
