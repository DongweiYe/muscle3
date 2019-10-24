/* This is a part of the integration test suite, and is run from a Python
 * test in /integration_test. It is not a unit test.
 */
#include <libmuscle/data.hpp>
#include <libmuscle/mcp/data_pack.hpp>
#include <libmuscle/mcp/message.hpp>
#include <libmuscle/mcp/client.hpp>
#include <libmuscle/mcp/tcp_client.hpp>
#include <ymmsl/ymmsl.hpp>

#include <cassert>
#include <memory>

#include <msgpack.hpp>


using libmuscle::impl::DataConstRef;
using libmuscle::impl::mcp::Message;
using libmuscle::impl::mcp::Client;
using libmuscle::impl::mcp::TcpClient;
using libmuscle::impl::mcp::unpack_data;
using ymmsl::Reference;
using ymmsl::Settings;


int main(int argc, char *argv[]) {
    // get server location from command line
    assert(argc == 2);
    std::string server_location(argv[1]);

    // start tcp client for the receiver
    assert(TcpClient::can_connect_to(server_location));

    Reference instance_id("test_receiver");
    std::shared_ptr<Client> client = std::make_unique<TcpClient>(instance_id, server_location);

    // receive a message
    Reference receiver("test_receiver.test_port2");
    DataConstRef bytes = client->receive(receiver);
    Message message = Message::from_bytes(bytes);

    // check message
    assert(message.sender == Reference("test_sender.test_port"));
    assert(message.receiver == receiver);
    assert(message.port_length == 10);
    assert(message.timestamp == 1.0);
    assert(message.next_timestamp == 2.0);

    auto overlay = message.settings_overlay.as<Settings>();
    assert(overlay["test_setting"].is_a<int64_t>());
    assert(overlay["test_setting"].as<int64_t>() == 42);

    assert(message.data.is_a_dict());
    assert(message.data["test1"].is_a<int>());
    assert(message.data["test1"].as<int>() == 10);
    assert(message.data["test2"].is_a_list());
    assert(message.data["test2"][0].is_nil());
    assert(message.data["test2"][1].as<bool>() == true);
    assert(message.data["test2"][2].as<std::string>() == "testing");

    return 0;
}

