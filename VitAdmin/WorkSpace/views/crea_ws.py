from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from models import WorkSpace, Team, Member, User  # Import User từ MySQL


# ==================== HELPER FUNCTIONS ====================

def validate_user_exists(us_id):
    """
    Kiểm tra user có tồn tại trong MySQL không
    """
    try:
        user = User.objects.get(us_id=us_id)
        return True, user
    except User.DoesNotExist:
        return False, None


def validate_users_exist(user_ids):
    """
    Kiểm tra nhiều users có tồn tại không
    Return: (success, invalid_users, valid_users)
    """
    invalid_users = []
    valid_users = []
    
    for us_id in user_ids:
        exists, user = validate_user_exists(us_id)
        if exists:
            valid_users.append(user)
        else:
            invalid_users.append(us_id)
    
    return len(invalid_users) == 0, invalid_users, valid_users


# ==================== WORKSPACE VIEWS ====================

@csrf_exempt
@require_http_methods(["POST"])
def create_workspace(request):
    """
    Tạo workspace mới
    
    Body JSON:
    {
        "ws_id": "ws_001",
        "ws_name": "Marketing Team Workspace",
        "owner_id": "user_123"
    }
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['ws_id', 'ws_name', 'owner_id']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Validate owner exists in MySQL
        owner_exists, owner = validate_user_exists(data['owner_id'])
        if not owner_exists:
            return JsonResponse({
                'success': False,
                'error': f'User with ID {data["owner_id"]} does not exist'
            }, status=404)
        
        # Check if workspace already exists
        if WorkSpace.objects(ws_id=data['ws_id']).first():
            return JsonResponse({
                'success': False,
                'error': 'Workspace with this ID already exists'
            }, status=400)
        
        # Create workspace
        workspace = WorkSpace(
            ws_id=data['ws_id'],
            ws_name=data['ws_name'],
            owner_id=data['owner_id']
        )
        workspace.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Workspace created successfully',
            'data': {
                'ws_id': workspace.ws_id,
                'ws_name': workspace.ws_name,
                'owner_id': workspace.owner_id,
                'owner_name': owner.us_name,
                'owner_email': owner.us_email
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_workspace(request, ws_id):
    """
    Lấy thông tin workspace theo ID (bao gồm thông tin owner từ MySQL)
    """
    try:
        workspace = WorkSpace.objects(ws_id=ws_id).first()
        
        if not workspace:
            return JsonResponse({
                'success': False,
                'error': 'Workspace not found'
            }, status=404)
        
        # Lấy thông tin owner từ MySQL
        owner_exists, owner = validate_user_exists(workspace.owner_id)
        
        response_data = {
            'ws_id': workspace.ws_id,
            'ws_name': workspace.ws_name,
            'owner_id': workspace.owner_id
        }
        
        if owner_exists:
            response_data['owner_info'] = {
                'us_name': owner.us_name,
                'us_email': owner.us_email,
                'us_img': owner.us_img
            }
        
        return JsonResponse({
            'success': True,
            'data': response_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def list_workspaces(request):
    """
    Lấy danh sách tất cả workspace của user
    Query params: owner_id
    """
    try:
        owner_id = request.GET.get('owner_id')
        
        if owner_id:
            workspaces = WorkSpace.objects(owner_id=owner_id)
        else:
            workspaces = WorkSpace.objects()
        
        data = []
        for ws in workspaces:
            owner_exists, owner = validate_user_exists(ws.owner_id)
            ws_data = {
                'ws_id': ws.ws_id,
                'ws_name': ws.ws_name,
                'owner_id': ws.owner_id
            }
            if owner_exists:
                ws_data['owner_name'] = owner.us_name
            data.append(ws_data)
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_workspace(request, ws_id):
    """
    Xóa workspace
    """
    try:
        workspace = WorkSpace.objects(ws_id=ws_id).first()
        
        if not workspace:
            return JsonResponse({
                'success': False,
                'error': 'Workspace not found'
            }, status=404)
        
        # Xóa tất cả teams trong workspace
        Team.objects(ws_id=ws_id).delete()
        
        workspace.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Workspace deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ==================== TEAM VIEWS ====================

@csrf_exempt
@require_http_methods(["POST"])
def create_team(request):
    """
    Tạo team trong workspace
    
    Body JSON:
    {
        "tm_id": "team_001",
        "tm_name": "Design Team",
        "tm_desc": "Team thiết kế UI/UX",
        "ws_id": "ws_001",
        "members": [
            {
                "role": "leader",
                "us_id": "user_123",
                "joined_at": "2025-11-06"
            },
            {
                "role": "member",
                "us_id": "user_456",
                "joined_at": "2025-11-06"
            }
        ]
    }
    """
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['tm_id', 'tm_name', 'ws_id']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }, status=400)
        
        # Check if workspace exists
        workspace = WorkSpace.objects(ws_id=data['ws_id']).first()
        if not workspace:
            return JsonResponse({
                'success': False,
                'error': 'Workspace not found'
            }, status=404)
        
        # Check if team already exists
        if Team.objects(tm_id=data['tm_id']).first():
            return JsonResponse({
                'success': False,
                'error': 'Team with this ID already exists'
            }, status=400)
        
        # Validate all members exist in MySQL
        members = []
        if 'members' in data and data['members']:
            member_ids = [m['us_id'] for m in data['members']]
            all_valid, invalid_users, valid_users = validate_users_exist(member_ids)
            
            if not all_valid:
                return JsonResponse({
                    'success': False,
                    'error': f'Following users do not exist: {", ".join(invalid_users)}'
                }, status=404)
            
            # Create members list
            for member_data in data['members']:
                member = Member(
                    role=member_data.get('role', 'member'),
                    us_id=member_data['us_id'],
                    joined_at=datetime.strptime(member_data['joined_at'], '%Y-%m-%d').date()
                )
                members.append(member)
        
        # Create team
        team = Team(
            tm_id=data['tm_id'],
            tm_name=data['tm_name'],
            tm_desc=data.get('tm_desc', ''),
            ws_id=data['ws_id'],
            members=members,
            created_at=datetime.now().date()
        )
        team.save()
        
        # Lấy thông tin chi tiết members từ MySQL
        members_info = []
        for member in members:
            _, user = validate_user_exists(member.us_id)
            if user:
                members_info.append({
                    'role': member.role,
                    'us_id': member.us_id,
                    'us_name': user.us_name,
                    'us_email': user.us_email,
                    'joined_at': member.joined_at.strftime('%Y-%m-%d')
                })
        
        return JsonResponse({
            'success': True,
            'message': 'Team created successfully',
            'data': {
                'tm_id': team.tm_id,
                'tm_name': team.tm_name,
                'tm_desc': team.tm_desc,
                'ws_id': team.ws_id,
                'created_at': team.created_at.strftime('%Y-%m-%d'),
                'members_count': len(team.members),
                'members': members_info
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_team(request, tm_id):
    """
    Lấy thông tin team theo ID (bao gồm thông tin chi tiết members từ MySQL)
    """
    try:
        team = Team.objects(tm_id=tm_id).first()
        
        if not team:
            return JsonResponse({
                'success': False,
                'error': 'Team not found'
            }, status=404)
        
        # Lấy thông tin chi tiết members từ MySQL
        members_data = []
        for member in team.members:
            user_exists, user = validate_user_exists(member.us_id)
            member_info = {
                'role': member.role,
                'us_id': member.us_id,
                'joined_at': member.joined_at.strftime('%Y-%m-%d')
            }
            if user_exists:
                member_info['us_name'] = user.us_name
                member_info['us_email'] = user.us_email
                member_info['us_img'] = user.us_img
            members_data.append(member_info)
        
        return JsonResponse({
            'success': True,
            'data': {
                'tm_id': team.tm_id,
                'tm_name': team.tm_name,
                'tm_desc': team.tm_desc,
                'ws_id': team.ws_id,
                'created_at': team.created_at.strftime('%Y-%m-%d'),
                'members': members_data
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def list_teams(request):
    """
    Lấy danh sách teams trong workspace
    Query params: ws_id
    """
    try:
        ws_id = request.GET.get('ws_id')
        
        if not ws_id:
            return JsonResponse({
                'success': False,
                'error': 'ws_id parameter is required'
            }, status=400)
        
        teams = Team.objects(ws_id=ws_id)
        
        data = [{
            'tm_id': team.tm_id,
            'tm_name': team.tm_name,
            'tm_desc': team.tm_desc,
            'created_at': team.created_at.strftime('%Y-%m-%d'),
            'members_count': len(team.members)
        } for team in teams]
        
        return JsonResponse({
            'success': True,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def add_member_to_team(request, tm_id):
    """
    Thêm thành viên vào team
    
    Body JSON:
    {
        "role": "member",
        "us_id": "user_789",
        "joined_at": "2025-11-06"
    }
    """
    try:
        data = json.loads(request.body)
        
        # Validate user exists in MySQL
        user_exists, user = validate_user_exists(data['us_id'])
        if not user_exists:
            return JsonResponse({
                'success': False,
                'error': f'User with ID {data["us_id"]} does not exist'
            }, status=404)
        
        team = Team.objects(tm_id=tm_id).first()
        if not team:
            return JsonResponse({
                'success': False,
                'error': 'Team not found'
            }, status=404)
        
        # Check if member already exists
        for member in team.members:
            if member.us_id == data['us_id']:
                return JsonResponse({
                    'success': False,
                    'error': 'User is already a member of this team'
                }, status=400)
        
        # Add new member
        new_member = Member(
            role=data.get('role', 'member'),
            us_id=data['us_id'],
            joined_at=datetime.strptime(data['joined_at'], '%Y-%m-%d').date()
        )
        
        team.members.append(new_member)
        team.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Member added successfully',
            'data': {
                'role': new_member.role,
                'us_id': new_member.us_id,
                'us_name': user.us_name,
                'us_email': user.us_email,
                'joined_at': new_member.joined_at.strftime('%Y-%m-%d')
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def remove_member_from_team(request, tm_id, us_id):
    """
    Xóa thành viên khỏi team
    """
    try:
        team = Team.objects(tm_id=tm_id).first()
        if not team:
            return JsonResponse({
                'success': False,
                'error': 'Team not found'
            }, status=404)
        
        # Find and remove member
        member_found = False
        removed_member = None
        for i, member in enumerate(team.members):
            if member.us_id == us_id:
                removed_member = team.members.pop(i)
                member_found = True
                break
        
        if not member_found:
            return JsonResponse({
                'success': False,
                'error': 'Member not found in team'
            }, status=404)
        
        team.save()
        
        # Lấy thông tin user từ MySQL
        user_exists, user = validate_user_exists(us_id)
        response_data = {
            'success': True,
            'message': 'Member removed successfully',
            'removed_member': {
                'us_id': us_id
            }
        }
        
        if user_exists:
            response_data['removed_member']['us_name'] = user.us_name
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_member_role(request, tm_id, us_id):
    """
    Cập nhật role của member trong team
    
    Body JSON:
    {
        "role": "leader"
    }
    """
    try:
        data = json.loads(request.body)
        
        team = Team.objects(tm_id=tm_id).first()
        if not team:
            return JsonResponse({
                'success': False,
                'error': 'Team not found'
            }, status=404)
        
        # Find and update member role
        member_found = False
        for member in team.members:
            if member.us_id == us_id:
                member.role = data.get('role', member.role)
                member_found = True
                break
        
        if not member_found:
            return JsonResponse({
                'success': False,
                'error': 'Member not found in team'
            }, status=404)
        
        team.save()
        
        # Lấy thông tin user từ MySQL
        user_exists, user = validate_user_exists(us_id)
        response_data = {
            'success': True,
            'message': 'Member role updated successfully',
            'data': {
                'us_id': us_id,
                'role': data.get('role')
            }
        }
        
        if user_exists:
            response_data['data']['us_name'] = user.us_name
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_team(request, tm_id):
    """
    Xóa team
    """
    try:
        team = Team.objects(tm_id=tm_id).first()
        
        if not team:
            return JsonResponse({
                'success': False,
                'error': 'Team not found'
            }, status=404)
        
        team.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Team deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)