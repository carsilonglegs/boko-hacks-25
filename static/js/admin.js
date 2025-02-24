// admin.js
function initializeApp() {
    const adminContainer = document.getElementById('app-container');
    
    // Initial HTML setup
    adminContainer.innerHTML = `
        <div class="w-full max-w-2xl mx-auto p-6">
            <div id="message-area"></div>
            <div id="login-section">
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h2 class="text-2xl font-bold mb-6 text-gray-800">Admin Login</h2>
                    <form id="admin-login-form" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Username:</label>
                            <input type="text" name="username" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Password:</label>
                            <input type="password" name="password" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                        </div>
                        <button type="submit" class="w-full bg-maroon-600 text-white p-2 rounded-md hover:bg-maroon-700">
                            Login
                        </button>
                    </form>
                </div>
            </div>
            <div id="admin-panel" style="display: none;">
                <div class="space-y-6">
                    <h2 class="text-2xl font-bold text-gray-800 text-center">Admin Management</h2>

                    <!-- Logout button moved to its own div to match Add User & Add Admin -->
                    <div class="flex flex-col space-y-4">
                        <button id="logout-button" class="btn">
                            Logout
                         </button>
                    </div>
                </div>
                    
                    <!-- User Management Section -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl font-semibold mb-4">User Management</h3>
                        <div id="user-list" class="space-y-3 mb-6"></div>
                        
                        <h4 class="text-lg font-semibold mb-2">Add New User</h4>
                        <form id="add-user-form" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Username:</label>
                                <input type="text" name="username" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Password:</label>
                                <input type="password" name="password" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                            </div>
                            <button type="submit" class="w-full bg-maroon-600 text-white p-2 rounded-md hover:bg-maroon-700">
                                Add User
                            </button>
                        </form>
                    </div>
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl font-semibold mb-4">Current Admins</h3>
                        <div id="admin-list" class="space-y-3"></div>
                    </div>
                    <div id="add-admin-section" class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="text-xl font-semibold mb-4">Add New Admin</h3>
                        <form id="add-admin-form" class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Username:</label>
                                <input type="text" name="username" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700">Password:</label>
                                <input type="password" name="password" required class="mt-1 block w-full rounded-md border border-gray-300 p-2">
                            </div>
                            <button type="submit" class="w-full bg-maroon-600 text-white p-2 rounded-md hover:bg-maroon-700">
                                Add Admin
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Show message in the message area
    function showMessage(message, type = 'error') {
        const messageArea = document.getElementById('message-area');
        messageArea.innerHTML = `
            <div class="p-4 mb-4 rounded ${type === 'error' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}">
                ${message}
            </div>
        `;
        setTimeout(() => messageArea.innerHTML = '', 3000);
    }

    // Update admin list display
    function updateAdminList(admins) {
        const adminList = document.getElementById('admin-list');
        adminList.innerHTML = admins.map(admin => `
            <div class="flex justify-between items-center p-3 bg-gray-50 rounded-md">
                <div>
                    <span class="font-medium">${admin[1]}</span>
                    ${admin[2] ? '<span class="ml-2 px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">Default Admin</span>' : ''}
                </div>
                ${!admin[2] ? `
                    <button onclick="window.removeAdmin(${admin[0]})" class="btn">
                        Remove
                    </button>
                ` : ''}
            </div>
        `).join('');
    }

    // Handle login form submission
    async function handleLogin(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        try {
            const response = await fetch('/admin', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                document.getElementById('login-section').style.display = 'none';
                document.getElementById('admin-panel').style.display = 'block';
                updateAdminList(data.admins);
                showMessage(data.message, 'success');// Directly injects html
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('An error occurred. Please try again.');
        }
    }

    // Handle adding new admin
    async function handleAddAdmin(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        try {
            const response = await fetch('/admin/add', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                updateAdminList(data.admins);
                form.reset();
                showMessage(data.message, 'success');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('An error occurred. Please try again.');
        }
    }

    // Handle removing admin
    window.removeAdmin = async function(adminId) {
        if (!confirm('Are you sure you want to remove this admin?')) return;

        try {
            const response = await fetch(`/admin/remove/${adminId}`, {
                method: 'POST'
            });
            const data = await response.json();

            if (data.success) {
                updateAdminList(data.admins);
                showMessage(data.message, 'success');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('An error occurred. Please try again.');
        }
    }

    // Handle logout
    async function handleLogout() {
        try {
            const response = await fetch('/admin/logout', {
                method: 'POST',  
                headers: { 'Content-Type': 'application/json' }
            });
    
            const data = await response.json();
    
            if (data.success) {
                document.getElementById('login-section').style.display = 'block';
                document.getElementById('admin-panel').style.display = 'none';
                showMessage('Logged out successfully', 'success');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('Failed to logout');
        }
    }
    

    // Function to update user list
    async function updateUserList() {
        try {
            const response = await fetch('/admin/users');
            const data = await response.json();

            console.log("User List API Response", data);
            
            if (data.success) {
                const userList = document.getElementById('user-list');
                userList.innerHTML = data.users.map(user => `
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-md">
                    <span class="font-medium">${user.username}</span>
                    <div class="space-x-2">
                        <button onclick="resetPassword(${user.id})" 
                                class="btn">
                            Reset Password
                        </button>
                        <button onclick="deleteUser(${user.id})"
                                class="btn">
                            Delete
                        </button>
                    </div>
                </div>  
                `).join('');
            }else{
                console.error("User list did not retrun success:",data);
            }
        } catch (error) {
            console.error("Error fetching users:",error);
            showMessage('Failed to load users');
        }
    }

    // Load users after successful login
function handleLoginSuccess(data) {
    document.getElementById('login-section').style.display = 'none';
    document.getElementById('admin-panel').style.display = 'block';
    updateAdminList(data.admins);
    updateUserList();  // Load the user list
    showMessage('Login successful', 'success');
}

// Handle adding new user
    async function handleAddUser(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        try {
            const response = await fetch('/admin/users/add', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                showMessage(data.message, 'success');
                form.reset();
                updateUserList();
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('Failed to add user');
        }
    }

    // Handle deleting user
    window.deleteUser = async function(userId) {
        if (!confirm('Are you sure you want to delete this user?')) return;

        try {
            const response = await fetch(`/admin/users/${userId}`, {
                method: 'DELETE'
            });
            const data = await response.json();

            if (data.success) {
                showMessage(data.message, 'success');
                updateUserList();
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('Failed to delete user');
        }
    }

    // Handle password reset
    window.resetPassword = async function(userId) {
        const newPassword = prompt('Enter new password:');
        if (!newPassword) return;

        try {
            const formData = new FormData();
            formData.append('user_id', userId);
            formData.append('new_password', newPassword);

            const response = await fetch('/admin/users/reset-password', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                showMessage(data.message, 'success');
            } else {
                showMessage(data.message);
            }
        } catch (error) {
            showMessage('Failed to reset password');
        }
    }

    // event listeners
    document.getElementById('admin-login-form').addEventListener('submit', handleLogin);
    document.getElementById('add-admin-form').addEventListener('submit', handleAddAdmin);
    document.getElementById('add-user-form').addEventListener('submit', handleAddUser);
    document.getElementById('logout-button').addEventListener('click', handleLogout);
    document.getElementById('close-modal').addEventListener('click', handleLogout)

    // Check initial login status
    fetch('/admin-check')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                document.getElementById('login-section').style.display = 'none';
                document.getElementById('admin-panel').style.display = 'block';
                updateAdminList(data.admins);
                updateUserList(); // Load user list on login
            }
        })
        .catch(error => {
            showMessage('Failed to check login status');
        });
}

// Make initialization function available globally
window.initializeApp = initializeApp;