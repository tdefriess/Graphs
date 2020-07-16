import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
            return False
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
            return False
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def fisher_yates_shuffle(self, l):
        for i in range(0, len(l)):
            random_index = random.randint(i, len(l) - 1)
            l[random_index], l[i] = l[i], l[random_index]

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        for user in range(num_users):
            self.add_user(user)

        friendships = []
        for user in range(1, self.last_id + 1):
            for friend in range(user + 1, num_users + 1):
                friendship = (user, friend)
                friendships.append(friendship)

        total_friendships = num_users * avg_friendships

        random_friendships = friendships[:total_friendships//2]

        for friendship in random_friendships:
            self.add_friendship(friendship[0], friendship[1])

        # Add users
        # use num_users

        # Create friendships
        # make a list with all POSSIBLE friendships

        ## Shuffle the list

        ## Take as many as we need

        ## add to self.friendships

    def linear_populate_graph(self, num_users, avg_friendships):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        for user in range(num_users):
            self.add_user(user)

        # linear way to add the number of friendships we need?
        # iterate for number of friendships to generate.
        # as long as we haven't made all the friendships we need
        # pick 2 random numbers between 1 and last id
        # try to create that frienship
        # if we can, increment friendships
        # for each, generate random pair.
        # check for existing pair. A little above linear.

        target_number_friendships = num_users * avg_friendships
        friendships_created = 0

        while friendships_created < target_number_friendships:
            friend_one = random.randint(1, self.last_id)
            friend_two = random.randint(1, self.last_id)

            friendship_was_made = self.add_friendship(friend_one, friend_two)

            if friendship_was_made:
                friendships_created += 2

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.

        Plan: BFT, use dictionary as visited
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = Queue()
        q.enqueue([user_id])

        while q.size() > 0:
            current_path = q.dequeue()

            current_user = current_path[-1]

            if current_user not in visited:
                visited[current_user] = current_path

                friends = self.friendships[current_user]

                for friend in friends:
                    path_to_friend = current_path + [friend]

                    q.enqueue(path_to_friend)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

    # what percentage of total users are in our extended social network?

    # how many people we know, divided by how many people there are

    print(f'{(len(connections) - 1) / 1000 * 100}%')

    # what is the average degree of separation between a user and those in his/her extended network?
    ## average length of a path to each user
    # traverse a user's extended connections, gather lengths, sum
    # divide by number of friends in connected component aka extended social network
    total_lengths = 0
    for friend in connections:
        total_lengths += len(connections[friend])

    print(f'Average degree of separation: {total_lengths / len(connections)}')